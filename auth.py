from flask import session
from werkzeug import check_password_hash, generate_password_hash


def user_get(username):
    """Get a user by username."""
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        raise ValueError('Invalid username')


def authenticate(username, password):
    """Attempt to log the user in. Raises a ValueError on bad credentials."""
    try:
        user = user_get(username)
    except ValueError as e:
        raise e
    else:
        if check_password_hash(user.pw_hash, password):
            session['user_id'] = user.user_id
        else:
            raise ValueError('Invalid password')


def user_create(username, password):
    """Create a user."""
    user = User(username, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
