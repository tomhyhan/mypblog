from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from myblog import db, create_myblog

app = create_myblog()

def manager():
    with app.app_context():
        migrate = Migrate(app, db)
        manager = Manager(app)

        manager.add_command('db', MigrateCommand)
        manager.run()

if __name__ == '__main__':
    manager()
