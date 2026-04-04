from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, ProfileForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.lower().strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created! Complete your profile to get stronger matches.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect(next_page or url_for("dashboard.index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been signed out.", "info")
    return redirect(url_for("main.home"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data.strip()
        current_user.last_name  = form.last_name.data.strip()
        current_user.university = form.university.data.strip()
        current_user.major      = form.major.data.strip()
        current_user.graduation = form.graduation.data.strip()
        current_user.gpa        = form.gpa.data.strip()
        current_user.location   = form.location.data.strip()
        current_user.work_auth  = form.work_auth.data
        current_user.skills     = form.skills.data.strip()
        current_user.github     = form.github.data.strip()
        current_user.linkedin   = form.linkedin.data.strip()
        current_user.portfolio  = form.portfolio.data.strip()
        current_user.bio        = form.bio.data.strip()
        db.session.commit()
        flash("Profile saved successfully.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("profile.html", form=form)