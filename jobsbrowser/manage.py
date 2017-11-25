from flask_script import (
    Manager,
    Server,
)

from api import app

manager = Manager(app)

manager.add_command("runserver", Server())


if '__main__' == __name__:
    manager.run()
