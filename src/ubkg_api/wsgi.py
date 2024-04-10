from app import UbkgAPI
from pathlib import Path

application = UbkgAPI('app.cfg', Path(__file__).absolute().parent.parent.parent).app

if __name__ == '__main__':
    application.run()
