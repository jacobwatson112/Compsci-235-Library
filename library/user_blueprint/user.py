from flask import Blueprint, render_template, url_for, session, redirect,request
from library.domain import model
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired
import library.adapters.abstractrepository as repo
from library.domain.model import User


user_blueprint = Blueprint('user_blueprint', __name__)

class SearchFrom(FlaskForm):
    search = StringField("Search", [DataRequired()])
    submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
    username = StringField("User name", [DataRequired()])
    password = StringField("Password", [DataRequired()])
    confirm = StringField("Confirm password", [DataRequired()])

    submit = SubmitField("Submit")


class SignInForm(FlaskForm):
    username = StringField("User name", [DataRequired()])
    password = StringField("Password", [DataRequired()])
    submit = SubmitField("Submit")


@user_blueprint.route('/sign_up', methods=["GET", "POST"])
def sign():
    search_form = SearchFrom()
    sign_up = SignUpForm()
    sign_in = SignInForm()
    if session.get('logged_in'):
        return redirect(url_for("book_blueprint.home"))
    return render_template('sign_up.html', sign_up=sign_up, sign_in=sign_in, search_form=search_form)

@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    sign_in = SignInForm(request.form)
    search_form = SearchFrom()
    sign_up = SignUpForm()
    if sign_in.validate_on_submit():
        print("SIGNING IN")
        user_name = sign_in.username.data
        password = sign_in.password.data
        user = repo.repo_instance.get_user(user_name)
        if user:
            if user.password == password:
                session['logged_in'] = True
                session['user'] = user_name
                return redirect(url_for("book_blueprint.home"))
            else:
                return render_template('sign_up.html', sign_up=sign_up, sign_in=sign_in, error="Incorrect password", search_form=search_form)
                pass
        else:
            return render_template('sign_up.html', sign_up=sign_up, sign_in=sign_in, error="user doesnt exist uwu", search_form=search_form)
            pass
    pass

@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    sign_up = SignUpForm(request.form)
    sign_in = SignInForm(request.form)
    search_form = SearchFrom()
    if sign_up.validate_on_submit():
        print("REGISTERING")
        user_name = sign_up.username.data
        password = sign_up.password.data
        confirm_password = sign_up.confirm.data
        if password == confirm_password:
            if repo.repo_instance.get_user(user_name):
                return render_template('sign_up.html', sign_up=sign_up, sign_in=sign_in, error="user already exists uwu dont steal someones identity :3", search_form=search_form)
                pass
            else:
                session['logged_in'] = True
                user = User(user_name, password)
                session['user'] = user_name
                repo.repo_instance.add_user(user)
                return redirect(url_for("book_blueprint.home"))
        else:
            return render_template('sign_up.html', sign_up=sign_up, sign_in=sign_in, error="youw passwowds dont mawtch.:3 check fow ewwows UwU", search_form=search_form)
            pass
    pass

@user_blueprint.route("/logout")
def logout():
    session['logged_in'] = False
    session['user'] = None
    return redirect(url_for("book_blueprint.home"))

@user_blueprint.route("/display_review")
def display_review():
    search_form = SearchFrom()
    if session.get("logged_in"):
        user = repo.repo_instance.get_user(session["user"])
        reviews = repo.repo_instance.get_reviews(user)
        return render_template("test_reviews_display.html", reviews=user.reviews, user=session.get("user"), search_form=search_form)
    else:
        return redirect(url_for('user_blueprint.sign'))