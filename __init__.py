import os
from pathlib import Path
from flask import Flask, render_template, request
from mandog.db import get_db
from flask_mail import Mail, Message

PATH = Path("mandog")

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
			DATABASE = os.path.join(app.instance_path, 'manblog.sqlite'),
			)
	app.config.from_pyfile('config.py', silent=True)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	mail = Mail()
	mail.init_app(app)

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import manblog
	app.register_blueprint(manblog.bp)

	@app.route('/')
	def home():
		db = get_db()
		posts = db.execute(
				'SELECT p.id, title, body, created, author_id,'
				' username FROM post p JOIN user u ON p.author_id ='
				' u.id ORDER BY created DESC LIMIT 10'
				).fetchall()
		return render_template('home.html', posts=posts)

	@app.route('/contact', methods=('GET', 'POST'))
	def contact():
		if request.method == 'POST':
			msg = Message(request.form['subject'], sender='mctestersontesty14@gmail.com', recipients=['dacrocs3@gmail.com'])
			msg.body = """
			From: %s <%s>
			%s
			""" % (request.form['name'], request.form['email'], request.form['msg'])
			mail.send(msg)
			return render_template('contact.html', success=True)
		elif request.method == 'GET':
			return render_template('contact.html')

	@app.route('/merch')
	def merch():
		return render_template('merch.html')

	@app.route('/about')
	def about():
		return render_template('about.html')

	@app.route('/shows')
	def shows():
		t = PATH / Path('static/resources/gallery/thumbnails')
		images = t.iterdir()
#		images = [i for i in os.listdir('static/resources/gallery/thumbnails')]
		return render_template('shows.html', images=images)

	return app
