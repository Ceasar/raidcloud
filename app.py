import os
from json_lib import jsonify, loads
from urllib2 import Request, urlopen, URLError
import webbrowser
import datetime
import pytz

from functools import wraps

import pbs

from flask import Flask, json, request, session, g, redirect, url_for, \
             render_template, flash
from flask_oauth import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug import secure_filename

from auth import authenticate
import dropbox

app = Flask(__name__)
app.config.from_object(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://raid:cloud@localhost/raidcloud'


app.config['GOOGLE_OAUTH_CONSUMER_KEY'] = '575198791092.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH_CONSUMER_SECRET'] = 'ei7THdOn1OyYCgYL_51ntTqK'
app.config['DROPBOX_OAUTH_CONSUMER_KEY'] = 'e7fbqqqwfb4zkyo'
app.config['DROPBOX_OAUTH_CONSUMER_SECRET'] = 'ohx5ci47pm717wh'
app.secret_key = 'ei7THdOn1OyYCgYL_51ntTqK'
db = SQLAlchemy(app)

oauth = OAuth()
google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive.file',
        'response_type': 'code'
        },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={
        'grant_type': 'authorization_code'
        },
    consumer_key=app.config['GOOGLE_OAUTH_CONSUMER_KEY'],
    consumer_secret=app.config['GOOGLE_OAUTH_CONSUMER_SECRET']
)


@google.tokengetter
def get_google_token():
    """Get the google OAuth token in form (token, secret).
    If no token exists, return None instead."""
    return session.get('google_token')


@app.route('/dropbox')
def dropbox_login():
    """Sign in with Dropbox."""
    app_key = app.config['DROPBOX_OAUTH_CONSUMER_KEY']
    app_secret = app.config['DROPBOX_OAUTH_CONSUMER_SECRET']

    sess = dropbox.session.DropboxSession(app_key, app_secret, 'app_folder')
    request_token = sess.obtain_request_token()
    session['dropbox_key'] = request_token

    next_url = request.args.get('next') or request.referrer
    callback = url_for('dropbox_oauth_authorized', next=next_url,
                           _external=True)
    url = sess.build_authorize_url(request_token, oauth_callback=callback)
    return redirect(url)


@app.route('/google')
def google_login():
    """Sign in with Google."""
    next_url = request.args.get('next') or request.referrer
    callback_url = url_for('google_oauth_authorized', next=next_url,
                           _external=True)
    return google.authorize(callback=callback_url)


def get_dropbox_client():
    if user.has_dropbox:
        sess = dropbox.session.DropboxSession(app.config['DROPBOX_OAUTH_CONSUMER_KEY'], app.config ['DROPBOX_OAUTH_CONSUMER_SECRET'], 'app_folder')
        sess.set_token(g.current_user.dropbox_id, g.current_user.dropbox_token)
        return dropbox.client.DropboxClient(sess)
    else:
        return None

@app.route('/dropbox_oauth_authorized')
def dropbox_oauth_authorized():
    """Store the oauth_token and secret and redirect."""

    app_key = app.config['DROPBOX_OAUTH_CONSUMER_KEY']
    app_secret = app.config['DROPBOX_OAUTH_CONSUMER_SECRET']

    sess = dropbox.session.DropboxSession(app_key, app_secret, 'app_folder')

    request_token = session['dropbox_key']
    access_token = sess.obtain_access_token(request_token)
    dropbox_id, dropbox_token = access_token.key, access_token.secret

    name = dropbox.client.DropboxClient(sess).account_info()['display_name']

    user = g.current_user or User.query.filter_by(dropbox_id=dropbox_id).first()
    if user:
        # Add/Update user dropbox creds
        if user.dropbox_token != dropbox_token:
            user.dropbox_token = dropbox_token
            user.dropbox_id = dropbox_id
            user.name = name
    else:
        # Create user
        user = User(dropbox_id=dropbox_id, dropbox_token=dropbox_token, name=name)
        db.session.add(user)

    db.session.commit()
    session['user_id'] = user.id

    return redirect(request.args.get('next') or url_for('index'))


@app.route('/set_session')
def set_session():
    session['user_id'] = 1
    return to_json(get_current_user())

@app.route('/google_oauth_authorized')
@google.authorized_handler
def google_oauth_authorized(resp):
    """Store the oauth_token and secret and redirect."""
    if resp is not None:
        drive_id = None
        drive_token = resp['access_token']

        headers = {'Authorization': 'OAuth ' + drive_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                      None, headers)
        res = json.loads(urlopen(req).read())
        """
        {
             "id": "117416155311954994698",
             "name": "Ceasar Bautista",
             "given_name": "Ceasar",
             "family_name": "Bautista",
             "link": "https://plus.google.com/117416155311954994698",
             "picture": "https://lh4.googleusercontent.com/-B2ePTSgN6G8/AAAAAAAAAAI/AAAAAAAAAKE/rCvvdkB3Mpo/photo.jpg",
             "gender": "male",
             "locale": "en-US"
        }
        """
        drive_id = res['id']
        name = res['name']

        user = g.current_user or User.query.filter_by(drive_id=drive_id).first()
        if user:
            # Add/Update user drive creds
            if user.drive_token != drive_token:
                user.drive_token = drive_token
                user.drive_id = drive_id
                user.name = name
        else:
            # Create user
            user = User(drive_id=drive_id, drive_token=drive_token, name=name)
            db.session.add(user)

        db.session.commit()
        session['user_id'] = user.id

    return redirect(request.args.get('next') or url_for('index'))


def get_current_user():
    """Convenience method to look up the current user's model"""
    try:
        return User.query.get(session['user_id'])
    except:
        return None

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    user = User.query.filter_by(username=username).first()
    return user.user_id if user else None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_current_user() is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def to_json(obj):
    _visited_objs = []
    def recurse(model):
        if isinstance(model.__class__, DeclarativeMeta):
            if model in _visited_objs:
                return None
            _visited_objs.append(model)

            fields = dict()
            for field in [x for x in dir(model) if not x.startswith('_') and x not in ['metadata', 'query', 'query_class']]:
                v = model.__getattribute__(field)
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0].__class__, DeclarativeMeta):
                    child_list = []
                    for child in v:
                        child_list.append(recurse(child))
                    fields[field] = child_list
                else:
                    fields[field] = recurse(v)
            return fields
        return model
    return jsonify(recurse(obj))

###
# Models
###


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(32), nullable=False, default='')

    drive_id = db.Column(db.String(255), nullable=True)
    drive_token = db.Column(db.String(255), nullable=True)

    dropbox_id = db.Column(db.String(255), nullable=True)
    dropbox_token = db.Column(db.String(255), nullable=True)

    files = db.relation('File', backref='user')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chunks = db.relation('Chunk', backref='file')
    modified_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now(tz=pytz.timezone('UTC')))


class Chunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    parity = db.Column(db.Boolean, nullable=False, default=False)
    service = db.Column(db.String(32), nullable=False)

###
# Routes
###


@app.before_request
def before_request():
    g.current_user = get_current_user()

@app.route('/')
@app.route('/account')
def index():
    return render_template('app.html')


@app.route('/user/<id>/files', methods=['POST'])
def upload():
    """Upload a file"""
    file = request.files['file']
    if file is not None:
        filename = secure_filename(file.filename)
        file.save(os.path.join('tmp', filename))
        handle_file(filename)


NUM_PARTS = 2

def handle_file(filename):
    """Split the file and upload its parts"""
    if filename is not None:
        pbs.sh('lxsplit-0.2.4/splitfile.sh', 'tmp/' + filename, NUM_PARTS)
    for i in [0..NUM_PARTS]:
        part_filename = "%s%02d" % (filename, i)


def put_dropbox(filename):
    """Put a file in the dropbox folder. User must be logged in."""
    app_key = app.config['DROPBOX_OAUTH_CONSUMER_KEY']
    app_secret = app.config['DROPBOX_OAUTH_CONSUMER_SECRET']
    sess = dropbox.session.DropboxSession(app_key, app_secret, 'app_folder')
    sess.set_token(g.current_user.dropbox_id, g.current_user.dropbox_token)
    client = dropbox.client.DropboxClient(sess)
    f = open(filename)
    client.put_file(filename, f)


@app.route('/foo')
def foo():
    try:
        show = [session['user_id'], g.current_user.dropbox_id]
        return str(show)
    except Exception as e:
        return str(e)


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
        if g.current_user:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/user')
@login_required
def user():
    user = g.current_user
    return to_json(user)


@app.route('/users')
def show_users():
    try:
        users = db.session.execute('SELECT id from "user"').fetchall()
        user_ids = [row[0] for row in users]
        return jsonify(users=user_ids)
    except:
        db.session.rollback()
        return jsonify({users: []})

@app.route('/users/<id>')
def show_user(id):
    return to_json(User.query.get(id))


@app.route('/files')
@login_required
def show_files(id):
    return {}


@app.route('/files/<id>')
@login_required
def show_file(id):
    return {}


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
