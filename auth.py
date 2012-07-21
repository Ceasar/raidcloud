

def authenticate(username, password):
    """Attempt to log the user in. Raises a ValueError on bad credentials."""
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError('Invalid username')
    if check_password_hash(user.pw_hash, password):
        session['user_id'] = user.user_id
    else:
        raise ValueError('Invalid password')


def user_create(username, password):
    """Create a user."""
    user = User(username, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
