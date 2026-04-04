import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Job, Application
from app.forms import get_application_form

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/")
def listing():
    q          = request.args.get("q", "").strip()
    role_type  = request.args.get("role_type", "")
    work_type  = request.args.get("work_type", "")
    experience = request.args.get("experience", "")

    query = Job.query.filter_by(is_active=True)

    if q:
        like = f"%{q}%"
        query = query.join(Job.company).filter(
            db.or_(Job.title.ilike(like),
                   Job.description.ilike(like),
                   Job.skills.ilike(like))
        )
    if role_type:
        query = query.filter_by(role_type=role_type)
    if work_type:
        query = query.filter_by(work_type=work_type)
    if experience:
        query = query.filter_by(experience=experience)

    jobs = query.order_by(Job.created_at.desc()).all()

    applied_ids = set()
    if current_user.is_authenticated:
        applied_ids = {a.job_id for a in current_user.applications.all()}

    role_types  = sorted({j.role_type  for j in Job.query.filter_by(is_active=True)})
    work_types  = sorted({j.work_type  for j in Job.query.filter_by(is_active=True)})
    experiences = sorted({j.experience for j in Job.query.filter_by(is_active=True)})

    return render_template("jobs.html", jobs=jobs, applied_ids=applied_ids,
                           role_types=role_types, work_types=work_types,
                           experiences=experiences,
                           q=q, selected_role=role_type,
                           selected_work=work_type, selected_exp=experience)


@jobs_bp.route("/<int:job_id>")
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    already_applied = False
    if current_user.is_authenticated:
        already_applied = Application.query.filter_by(
            user_id=current_user.id, job_id=job_id).first() is not None
    return render_template("job_detail.html", job=job, already_applied=already_applied)


@jobs_bp.route("/<int:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)

    existing = Application.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if existing:
        flash("You've already applied to this role.", "info")
        return redirect(url_for("dashboard.index"))

    FormClass = get_application_form(job.role_type)
    form = FormClass()

    if form.validate_on_submit():
        answers = {}
        for field in form:
            if field.name not in ("csrf_token", "submit", "cover_note"):
                answers[field.name] = field.data

        app_obj = Application(
            user_id    = current_user.id,
            job_id     = job_id,
            cover_note = form.cover_note.data,
            answers    = json.dumps(answers),
            status     = "Submitted",
        )
        db.session.add(app_obj)
        db.session.commit()
        flash(f"Application submitted to {job.company.name}! Good luck 🚀", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("apply.html", form=form, job=job)