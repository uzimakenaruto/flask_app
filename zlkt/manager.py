from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zlkt import app
from exts import db

# initialize Manager
manager = Manager(app)
# initialize Migrate
migrate = Migrate(app, db)
# 'db' is command prefix
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

