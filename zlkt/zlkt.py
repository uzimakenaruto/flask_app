from flask import Flask, render_template, request
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
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        pass


if __name__ == '__main__':
    app.run()
