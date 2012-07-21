import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, \
             render_template, flash
from flask.ext.oauth import OAuth

from auth import authenticate
# TODO: Make models file

app = Flask(__name__)
app.config.from_object(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://raid:cloud@localhost/raidcloud'

app.config['GOOGLE_OAUTH_CONSUMER_SECRET'] = 'ei7THdOn1OyYCgYL_51ntTqK'
app.config['GOOGLE_OAUTH_CONSUMER_KEY'] = 'AIzaSyAwJ0XdL2X6jU9S-2vOzfXsE3yfnx6361Q'
db = SQLAlchemy(app)

oauth = OAuth()
google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    request_token_url='https://www.google.com/accounts/OAuthGetRequestToken',
    access_token_url='https://www.google.com/accounts/OAuthGetAccessToken',
    authorize_url='https://www.google.com/accounts/OAuthAuthorizeToken',
    consumer_key=app.config['GOOGLE_OAUTH_CONSUMER_KEY'],
    consumer_secret=app.config['GOOGLE_OAUTH_CONSUMER_SECRET'],
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/drive.file'
    },
)


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    user = User.query.filter_by(username=username).first()
    return user.user_id if user else None

###
# Models
###


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    drive_id = db.Column(db.BigInteger, nullable=True)
    drive_token = db.Column(db.String(255), nullable=True)

    dropbox_id = db.Column(db.BigInteger, nullable=True)
    dropbox_token = db.Column(db.String(255), nullable=True)

    files = db.relation('File', backref='user')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chunks = db.relation('Chunk', backref='file')


class Chunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    parity = db.Column(db.Boolean, nullable=False, default=False)

###
# Routes
###


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()


@app.route('/')
def index():
    return render_template('app.html')
    # return 'Hello World!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            user_create(request.form['username'], request.form['password'])
            authenticate(request.form['username'], request.form['password'])
            return redirect(url_for('settings'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            authenticate(request.form['username'], request.form['password'])
        except ValueError as e:
            return render_template('login.html', error=str(e))
        else:
            flash('You were logged in')
            return redirect(url_for('index'))
    else:
        if g.user:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/users')
def show_users(id):
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
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
