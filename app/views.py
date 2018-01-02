from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import LoginForm, SignupForm, PostForm
from app.models import UserModel, PostModel


@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("my_posts"))
    else:
        return redirect(url_for("index"))


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = UserModel.query.filter_by(username=login_form.username.data).first()
        if user is not None and check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for("dashboard"))
        else:
            return "<h1>Invalid username or password!</h1>"
        # return "<h1>{0} {1}</h1>".format(form.username.data, form.password.data)

    return render_template("login.html", form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        new_user = UserModel(
            email=signup_form.email.data,
            username=signup_form.username.data,
            password=generate_password_hash(signup_form.password.data, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()

        return "<h1>User {0} has been created!</h1>".format(signup_form.username.data)

    return render_template("signup.html", form=signup_form)


@app.route("/dashboard")
@login_required
def dashboard():
    kwargs = {
        "name": current_user.username
    }
    return render_template("dashboard.html", **kwargs)


@app.route("/new_post", methods=["GET", "POST"])
@login_required
def create_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
        new_post = PostModel(
            header=post_form.header.data,
            body=post_form.body.data,
            user_id=current_user.id,
        )
        db.session.add(new_post)
        db.session.commit()

        return "<h1>New post has been created!</h1>"

    return render_template("new_post.html", form=post_form)


@app.route("/my_posts", methods=["GET"])
def usere_posts():

    posts = PostModel.query.filter_by(user_id=current_user.id)

    kwargs = {
        "username": current_user.username,
        "posts": posts,
    }

    return render_template("my_posts.html", **kwargs)
