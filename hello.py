import os
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://{0}/users.db'.format(os.path.dirname(__file__))

db = SQLAlchemy(app)


class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	
	def __repr__(self):
		return '<User %r>' % self.username

def init_db():
    db.create_all(app=app)





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
	user = Users.query.filter_by(username='Wicher').first()
	return render_template('index.html', name=user)

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()
    init_db()

