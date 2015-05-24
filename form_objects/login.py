from flask_wtf import Form
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(Form):
    email = EmailField('Enter your e-mail', [DataRequired()])
    password = PasswordField('Enter your password', [DataRequired()])
