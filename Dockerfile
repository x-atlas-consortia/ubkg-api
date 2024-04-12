# Parent image
FROM redhat/ubi9:9.3

LABEL description="Data Distillary UBKG API"

# Change to directory that contains the Dockerfile
WORKDIR /usr/src/app

# Copy from host to image
COPY . .

# When trying to run "yum updates" or "yum install" the "system is not registered with an entitlement server" error message is given
# To fix this issue:
RUN echo $'[main]\n\
enabled=0\n\\n\
# When following option is set to 1, then all repositories defined outside redhat.repo will be disabled\n\
# every time subscription-manager plugin is triggered by dnf or yum\n\
disable_system_repos=0\n'\
>> /etc/yum/pluginconf.d/subscription-manager.conf

# http://nginx.org/en/linux_packages.html#RHEL-CentOS
# Set up the yum repository to install the latest mainline version of Nginx
RUN echo $'[nginx-mainline]\n\
name=nginx mainline repo\n\
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/\n\
gpgcheck=1\n\
enabled=0\n\
gpgkey=https://nginx.org/keys/nginx_signing.key\n\
module_hotfixes=true\n'\
>> /etc/yum.repos.d/nginx.repo

# redhat/ubi9:9.3 comes with python3 in /usr/bin/python3. But install using
# alternatives as /usr/bin/python as highest priority alternative.
# alternatives --install /usr/bin/python python /usr/bin/python3.9 0
#
# Do we need other stuff like python3-requests?
# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/installing_and_using_dynamic_programming_languages/assembly_installing-and-using-python_installing-and-using-dynamic-programming-languages#doc-wrapper
#
# Reduce the number of layers in image by minimizing the number of separate RUN commands
# 1 - Install GCC, Git, Python 3.9, libraries needed for Python development, and pcre needed by uwsgi
# 2 - Set default Python version for `python` command, `python3` already points to the newly installed Python3.9
# 3 - Upgrade pip, after upgrading, both pip and pip3 are the same version
# 4 - Pip install wheel and uwsgi packages. Pip uses wheel to install uwsgi
# 5 - Clean all yum cache
RUN yum install -y gcc git python39 python3-devel pcre pcre-devel && \
    alternatives --install /usr/bin/python python /usr/bin/python3.9 0 && \
    dnf install python3-pip && \
    pip3 install --upgrade pip && \
    pip install wheel uwsgi && \
    yum clean all 

RUN yum install -y yum-utils && \
    yum-config-manager --enable nginx-mainline && \
    yum install -y nginx && \
    rm /etc/nginx/conf.d/default.conf && \
    mv nginx/nginx.conf /etc/nginx/nginx.conf && \
    rm -rf nginx && \
    pip install --upgrade pip -r src/ubkg_api/requirements.txt && \
    chmod +x start.sh && \
    yum clean all

# Install gosu for de-elevating from root to the user which will
# execute the startup script in entrypoint.sh
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.14/gosu-amd64" && \
    curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.14/gosu-amd64.asc" && \
    rm -r /usr/local/bin/gosu.asc && \
    chmod +x /usr/local/bin/gosu

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# EXPOSE does not make the ports of the container accessible to the host.
# Here 5000 is for the uwsgi socket, 8080 for nginx
EXPOSE 5000 8080

# Set an entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["./start.sh"]
