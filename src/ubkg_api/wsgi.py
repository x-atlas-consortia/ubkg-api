from app import UbkgAPI

application = UbkgAPI('./app.cfg').app

if __name__ == '__main__':
    application.run()

