import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://raid:cloud@localhost/raidcloud'


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/users')
def show_user(id):
    return {}


@app.route('/users/<id>')
def show_user(id):
    return {}


@app.route('/files')
def show_files(id):
    return {}


@app.route('/files/<id>')
def show_file(id):
    return {}


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
