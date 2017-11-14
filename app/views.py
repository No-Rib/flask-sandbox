from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import UserModel


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("dashboard"))
        else:
            return "<h1>Invalid username or password!</h1>"
        # return "<h1>{0} {1}</h1>".format(form.username.data, form.password.data)

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        new_user = UserModel(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(form.password.data, method="sha256")
        )
        db.session.add(new_user)
        db.session.commit()

        return "<h1>User {0} has been created!</h1>".format(form.username.data)

    return render_template("signup.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    kwargs = {
        "name": current_user.username
    }
    return render_template("dashboard.html", **kwargs)
