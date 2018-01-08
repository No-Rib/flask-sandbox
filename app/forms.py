from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("remember me")


class SignupForm(FlaskForm):
    email = StringField("email", validators=[
        InputRequired(), Email(message="Invalid email"), Length(max=50)
    ])
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=4, max=80)])


class PostForm(FlaskForm):
    header = StringField("header", validators=[InputRequired(), Length(min=1, max=80)])
    body = StringField("body", validators=[InputRequired(), Length(min=1, max=500)])
    tags = StringField("tags", validators=[Length(max=500)])
