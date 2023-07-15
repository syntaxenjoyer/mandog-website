import functools
from flask import (
		Blueprint, flash, g , render_template, redirect, request, session, url_for
		)
from werkzeug.security import check_password_hash
from mandog.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
				'SELECT * FROM user WHERE username = ?', (username,)
				).fetchone()

		if user is None:
			error = 'Unacceptable. I am disappointed.'
		elif not check_password_hash(user['password'], password):
			error = 'What the hell man. Get it together.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('manblog.create'))

		flash(error)	
	
	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
				'SELECT * FROM user WHERE id = ?', (user_id,)
				).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('home'))

		return view(**kwargs)

	return wrapped_view
