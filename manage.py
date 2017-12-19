from flask_script import (
    Manager,
    Server,
)

from jobsbrowser.api import init_app

manager = Manager(init_app)

manager.add_command("runserver", Server())


if '__main__' == __name__:
    manager.run()
