from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import db, login_manager


class User(db.Model, UserMixin):
    """Class for user objects"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        """Initialize user object"""
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Generate password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Compares two password hashes"""
        return check_password_hash(self.password_hash, password)


class RegistrationForm(FlaskForm):
    """Class for registering a new user when submitted"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Checks input username against existing usernames in database"""
        user = classes.User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Checks input email address against
         existing email addresses in database"""
        user = classes.User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    """Class for logging in a user when submitted"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class UploadFileForm(FlaskForm):
    """Class for uploading file when submitted"""
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')



db.create_all()
db.session.commit()

# user_loader :
# This callback is used to reload the user object
# from the user ID stored in the session.


@login_manager.user_loader
def load_user(id):
    """Reload the user object from the user ID stored in the session"""
    return User.query.get(int(id))
