import os
from json_lib import jsonify, loads
from urllib2 import Request, urlopen, URLError
import webbrowser
import datetime
import pytz
import subprocess

from functools import wraps

import pbs

import requests
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

    next_url = None
    callback = url_for('dropbox_oauth_authorized', next=next_url,
                           _external=True)
    url = sess.build_authorize_url(request_token, oauth_callback=callback)
    return redirect(url)


@app.route('/google')
def google_login():
    """Sign in with Google."""
    next_url = None
    callback_url = url_for('google_oauth_authorized', next=next_url,
                           _external=True)
    return google.authorize(callback=callback_url)


def get_dropbox_client():
    if g.current_user.has_dropbox:
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
    quota = dropbox.client.DropboxClient(sess).account_info()['quota_info']['quota']
    normal = dropbox.client.DropboxClient(sess).account_info()['quota_info']['normal']
    shared = dropbox.client.DropboxClient(sess).account_info()['quota_info']['shared']
    total = normal + shared

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
    if not user.dropbox_quota:
        user.dropbox_quota = quota
        user.dropbox_total = total

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
        user.drive_total = 5368709
        user.drive_quota = 5368709120

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
    drive_quota = db.Column(db.BigInteger, nullable=True)
    drive_total = db.Column(db.BigInteger, nullable=True)

    dropbox_id = db.Column(db.String(255), nullable=True)
    dropbox_token = db.Column(db.String(255), nullable=True)
    dropbox_quota = db.Column(db.BigInteger, nullable=True)
    dropbox_total = db.Column(db.BigInteger, nullable=True)

    files = db.relation('File', backref='user')

    @property
    def has_dropbox(self):
        return self.dropbox_id is not None

    @property
    def has_google(self):
        return self.drive_id is not None



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
    service = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    drive_id = db.Column(db.Integer, nullable=True)


###
# Routes
###


@app.before_request
def before_request():
    g.current_user = get_current_user()

@app.route('/')
@app.route('/account')
@login_required
def index():
    return render_template('index.html')


@app.route('/users/<id>/files', methods=['GET','POST'])
@login_required
def upload(id):
    if request.method == 'GET':
        files = User.query.get(id).files
    else:
        """Upload a file"""
        print request
        uploaded_file = request.files['file']
        if uploaded_file is not None:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join('tmp', filename))

            date = request.form.get('lastModifiedDate')
            date_parts = date.split(' ')
            parsed_date = ' '.join(date_parts[0:-2])

            _file = File(name=filename, size=request.form.get('bytes'), modified_at=parsed_date, user=g.current_user)
            db.session.add(_file)
            db.session.commit()

            split_file(_file)
            return jsonify({'success': True})
        return jsonify({'success': False})

@app.route('/users/<user_id>/files/<file_id>', methods=['GET'])
@login_required
def get_file(user_id, file_id):
    return to_json(File.query.get(file_id))


@app.route('/users/<user_id>/files/<file_id>/download', methods=['GET'])
@login_required
def download_file(user_id, file_id):
    _file = File.query.get(file_id)
    chunks = _file.chunks
    for chunk in chunks:
        if chunk.service is 'dropbox':
            get_dropbox(chunk)
        else:
            get_drive(chunk)
    data = []
    for i in xrange(1, NUM_PARTS+1):
        part_filename = "%s.%d" % (_file.name, i)
        f = open('tmp/' + part_filename, 'rb')
        data.append(f.read())
        f.close()

    f = open('tmp/' + _file.name, 'wb')
    for datum in data:
        f.write(data)

    return Response(f.read(), mimetype='application/binary')

NUM_PARTS = 2

def split_file(_file):
    """Split the file and upload its parts"""
    if _file is not None:
        f = open('tmp/' + _file.name, 'rb')
        data = f.read()
        f.close()

        bytes = len(data)
        inc = (bytes+2)/2
        num = 1
        for i in xrange(0, bytes+1, inc):
            fn1 = 'tmp/' + str(_file.name) + '.' + str(num)
            f = open(fn1, 'wb')
            f.write(data[i:i+inc])
            f.close()
            num += 1

        # Fail 2
        #os.chdir('tmp')
        #size = os.path.getsize(_file.name)
        #chunk_size = (size + NUM_PARTS - 1) / NUM_PARTS
        #subprocess.call(['../lxsplit-0.2.4/lxsplit', '-s', '../tmp/' + _file.name, str(chunk_size) + 'b'])
        #os.remove(_file.name)
        #os.chdir('../')

        # Fail 1
        #os.chdir('lxsplit-0.2.4')
        #os.popen('./splitfile.sh %s %d' % (_file.name, NUM_PARTS))
        #os.chdir('../')
    for i in xrange(1, NUM_PARTS+1):
        part_filename = "%s.%d" % (_file.name, i)
        chunk = Chunk(file=_file, parity=False, name=part_filename)
        db.session.add(chunk)
        db.session.commit()
        if i % 2 == 0:
            put_dropbox(chunk)
        else:
            put_drive(chunk)


def put_dropbox(chunk):
    """Put a file in the dropbox folder. User must be logged in."""
    client = get_dropbox_client()
    if client:
        f = open('tmp/' + chunk.name)
        client.put_file(chunk.name, f)
        chunk.service = 'dropbox'
        db.session.commit()


def get_dropbox(chunk):
    """Get a file from the dropbox folder. User must be logged in."""
    client = get_dropbox_client()
    if client:
        out = open('tmp/' + chunk.name, 'w')
        response = client.get_file(chunk.name)
        out.write(response.read())


def get_drive(chunk):
    drive_token = g.current_user.drive_token
    url = "https://www.googleapis.com/upload/drive/v2/files/" + chunk.drive_id
    headers = {
        'Authorization': 'OAuth ' + drive_token
    }
    data = None
    resp = requests.get(url, data=data, headers=headers)
    downloadURL = resp.json['downloadUrl']
    response = requests.get(downloadURL, data=data, headers=headers)
    out = open('tmp/' + chunk.name, 'w')
    out.write(response.read())


def put_drive(chunk):
    # drive_token = g.current_user.drive_token
    drive_token = g.current_user.drive_token
    url = "https://www.googleapis.com/upload/drive/v2/files?uploadType=media"
    data = open('tmp/' + chunk.name).read()
    headers = {
        'Content-Type': '',
        'Authorization': 'OAuth ' + drive_token
    }
    chunk.service = 'drive'
    db.session.commit()
    response = requests.post(url, data=data, headers=headers)
    chunk.drive_id = response.json['id']
    db.session.commit()

@app.route('/foo')
def foo():
    try:
        resp = put_drive('app.py')
        return str(resp)
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
