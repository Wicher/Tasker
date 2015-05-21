import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.auth import Auth
from form_objects.login import LoginForm
from pprint import pprint
from flask.ext.login import LoginManager, login_user

WTF_CSRF_SECRET_KEY = 'a random string'
WTF_CSRF_ENABLED = False


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True
auth = Auth(app)
login_manager = LoginManager()
login_manager.init_app(app)

manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://{0}/users.db'.format(os.path.dirname(__file__))

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return self.username

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

def init_db():
    db.create_all(app=app)

@login_manager.user_loader
def load_user(userid):
    # return Users.get_id(userid)
    return Users.query.filter_by(username=userid).first()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    pprint(e)
    return render_template('500.html'), 500


@app.route('/')
def index():
	# user = Users.query.filter_by(username='Wicher').first()
	return render_template('index.html', name=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        # user = Users.query.filter_by(username=request.form['email']).first()
        user = load_user(request.form['email'])
        if user and user.password == request.form['password']:
            login_user(user, force=True)
            return redirect(url_for('user', name=user))

    return render_template('login.html', form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    init_db()
    manager.run()



