# Dockerfile for UBKGBox ubkg-front-end service container build

# The ubkg-api is not deployed as a standalone component.
# It is either compiled as a PyPI package and consumed by child APIs (e.g., hs-ontology-api) or
# as a component of the UBKGBox Compose application.
# ---------------------------

# The parent image is based on RedHat Linux Universal Base Image (UBI).
FROM redhat/ubi9:9.4

# image LABEL layer
LABEL description="UBKGBox ubkg-front-end"

# -----------------
# INSTALL SYSTEM PACKAGES VIA YUM

# When trying to run "yum updates" or "yum install" the "system is not registered with an entitlement server" error message is given
# To fix this issue:
RUN echo $'[main]\n\
enabled=0\n\\n\
# When following option is set to 1, then all repositories defined outside redhat.repo will be disabled\n\
# every time subscription-manager plugin is triggered by dnf or yum\n\
disable_system_repos=0\n'\
>> /etc/yum/pluginconf.d/subscription-manager.conf

# Reduce the number of layers in the image by minimizing the number of separate RUN commands.
# 1 - Install GCC, Git, Python, and libraries needed for Python development.
# 2 - Set default Python version for `python` command, `python3` already points to the newly installed Python3.9.
# 3 - Upgrade pip, after upgrading, both pip and pip3 are the same version.
# 4 - Pip install wheel and uwsgi packages. Pip uses wheel to install uwsgi.
# 5 - Clean all yum cache.

RUN yum update -y && \
    yum install -y yum-utils && \
    yum install -y gcc git python python-devel && \
    python -m ensurepip --upgrade && \
    pip install wheel uwsgi && \
    yum clean all

# Install su-exec to allow running nginx from a non-root user.
# N.B. git and gcc are also needed for su-exec installation, but since already
#      added for uwsgi, they are simply used and are not removed like compilation-only packages.
WORKDIR /tmp
RUN yum install --assumeyes  procps-ng make && \
    git clone https://github.com/ncopa/su-exec.git /tmp/su-exec && \
    cd su-exec && \
    make && \
    mv su-exec /usr/local/bin/ && \
    chmod a+x /usr/local/bin/su-exec && \
    cd /tmp && \
    rm -Rf /tmp/su-exec/ && \
    yum remove --assumeyes make && \
    yum clean all

# ----------------
# INSTALL NGINX AND FLASK APP DEPENDENCIES VIA YUM.

# Change to directory that contains the Dockerfile.
WORKDIR /usr/src/app
COPY . .

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

# Reduce the number of layers in image by minimizing the number of separate RUN commands
# 1 - Install the prerequisites.
# 2 - By default, the repository for stable nginx packages is used. Use mainline nginx packages.
# 3 - Install nginx (using the custom yum repo specified earlier).
# 4 - Remove the default nginx config file.
# 5 - Overwrite the nginx.conf with ours to run nginx as non-root. Copy over conf.d.
# 6 - Remove the nginx directory copied from host machine (nginx/conf.d gets mounted to the container).
# 7 - Upgrade pip (the one installed in base image may be old) and install flask app dependencies (pip3 also works).
# 8 - Install Flask app dependencies.
# 9 - Make the start script executable.
# 10 - Clean all yum cache.

# RUN yum install -y yum-utils && \
RUN yum-config-manager --enable nginx-mainline && \
    yum install -y nginx && \
    rm /etc/nginx/conf.d/default.conf && \
    mv nginx/nginx.conf /etc/nginx/nginx.conf && \
    mv nginx/conf.d /etc/nginx &&\
    rm -rf nginx && \
    pip install --upgrade pip -r src/requirements.txt && \
    chmod +x start.sh && \
    yum clean all

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# EXPOSE does not make the ports of the container accessible to the host.
# 5000: nginx http socket defined in uswgi.ini
# 8080: HTTP
EXPOSE 5000 8080

# Set an entrypoint that configures nginx to run under a non-root user.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Start Nginx and uwsgi.
CMD ["./start.sh"]
