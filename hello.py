import os
import pdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.auth import Auth
from form_objects.login import LoginForm
from pprint import pprint
from flask.ext.login import LoginManager, login_user, logout_user, login_required, UserMixin

WTF_CSRF_SECRET_KEY = 'a random string'
WTF_CSRF_ENABLED = False

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://{0}/users.db'.format(os.path.dirname(__file__))
app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
auth = Auth(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

def init_db():
    db.create_all(app=app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    pprint(e)
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=request.form['email']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    init_db()
    manager.run()



