from flask import Flask
import config
from exts import db

# initialize a Flask object with argument __name__
app = Flask(__name__)
# import configuration file to set config properties
app.config.from_object(config)
# SQLAlchemy from flask-sqlalchemy moudule has a instanse db
# db initialized with no argument ,so need init_app(app)
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
