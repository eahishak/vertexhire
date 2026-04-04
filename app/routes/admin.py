from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from app.models import Application, Job, User, Company, APPLICATION_STATUSES

admin_bp = Blueprint("admin", __name__)


def require_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


# ── overview ──────────────────────────────────────────────────
@admin_bp.route("/")
@login_required
def index():
    require_admin()

    total_apps   = Application.query.count()
    total_users  = User.query.filter_by(is_admin=False).count()
    total_jobs   = Job.query.filter_by(is_active=True).count()
    total_offers = Application.query.filter_by(status="Offer").count()

    recent_apps  = (Application.query
                    .order_by(Application.submitted_at.desc())
                    .limit(8).all())

    status_counts = {s: Application.query.filter_by(status=s).count()
                     for s in APPLICATION_STATUSES}

    # apps per job for top roles
    top_jobs = (db.session.query(Job.title, Company.name, func.count(Application.id).label("cnt"))
                .join(Application, Application.job_id == Job.id)
                .join(Company, Company.id == Job.company_id)
                .group_by(Job.id)
                .order_by(func.count(Application.id).desc())
                .limit(5).all())

    return render_template("admin/index.html",
                           total_apps=total_apps,
                           total_users=total_users,
                           total_jobs=total_jobs,
                           total_offers=total_offers,
                           recent_apps=recent_apps,
                           status_counts=status_counts,
                           top_jobs=top_jobs)


# ── applications list ──────────────────────────────────────────
@admin_bp.route("/applications")
@login_required
def applications():
    require_admin()
    status_filter = request.args.get("status", "")
    job_filter    = request.args.get("job_id", "")

    q = Application.query
    if status_filter:
        q = q.filter_by(status=status_filter)
    if job_filter:
        q = q.filter_by(job_id=int(job_filter))

    apps = q.order_by(Application.submitted_at.desc()).all()
    jobs = Job.query.order_by(Job.title).all()

    return render_template("admin/applications.html",
                           applications=apps, jobs=jobs,
                           statuses=APPLICATION_STATUSES,
                           selected_status=status_filter,
                           selected_job=job_filter)


# ── single application ─────────────────────────────────────────
@admin_bp.route("/applications/<int:app_id>")
@login_required
def view_application(app_id):
    require_admin()
    app = Application.query.get_or_404(app_id)
    import json
    answers = {}
    if app.answers:
        try:
            answers = json.loads(app.answers)
        except Exception:
            pass
    return render_template("admin/view_application.html",
                           app=app, answers=answers,
                           statuses=APPLICATION_STATUSES)


# ── update status (POST) ───────────────────────────────────────
@admin_bp.route("/applications/<int:app_id>/status", methods=["POST"])
@login_required
def update_status(app_id):
    require_admin()
    app        = Application.query.get_or_404(app_id)
    new_status = request.form.get("status")
    if new_status in APPLICATION_STATUSES:
        app.status = new_status
        db.session.commit()
        flash(f"Moved to '{new_status}'.", "success")
    else:
        flash("Invalid status.", "danger")
    return redirect(url_for("admin.view_application", app_id=app_id))


# ── candidates ─────────────────────────────────────────────────
@admin_bp.route("/candidates")
@login_required
def candidates():
    require_admin()
    users = (User.query.filter_by(is_admin=False)
             .order_by(User.created_at.desc()).all())
    return render_template("admin/candidates.html", users=users)


# ── single candidate ───────────────────────────────────────────
@admin_bp.route("/candidates/<int:user_id>")
@login_required
def view_candidate(user_id):
    require_admin()
    user = User.query.get_or_404(user_id)
    apps = user.applications.order_by(Application.submitted_at.desc()).all()
    return render_template("admin/view_candidate.html", user=user, applications=apps)


# ── analytics ──────────────────────────────────────────────────
@admin_bp.route("/analytics")
@login_required
def analytics():
    require_admin()

    # total metrics
    total_apps    = Application.query.count()
    total_users   = User.query.filter_by(is_admin=False).count()
    total_offers  = Application.query.filter_by(status="Offer").count()
    total_reject  = Application.query.filter_by(status="Rejected").count()

    # offer rate
    offer_rate = round((total_offers / total_apps * 100), 1) if total_apps else 0

    # status breakdown
    status_data = {s: Application.query.filter_by(status=s).count()
                   for s in APPLICATION_STATUSES}

    # applications per role type
    role_data = (db.session.query(Job.role_type, func.count(Application.id).label("cnt"))
                 .join(Application, Application.job_id == Job.id)
                 .group_by(Job.role_type)
                 .all())

    # applications per company
    company_data = (db.session.query(Company.name, func.count(Application.id).label("cnt"))
                    .join(Job, Job.company_id == Company.id)
                    .join(Application, Application.job_id == Job.id)
                    .group_by(Company.id)
                    .order_by(func.count(Application.id).desc())
                    .all())

    # daily signups — last 14 days
    days     = 14
    today    = datetime.utcnow().date()
    signup_trend = []
    for i in range(days - 1, -1, -1):
        d     = today - timedelta(days=i)
        count = User.query.filter(
            func.date(User.created_at) == d,
            User.is_admin == False
        ).count()
        signup_trend.append({"date": d.strftime("%b %d"), "count": count})

    # daily applications — last 14 days
    app_trend = []
    for i in range(days - 1, -1, -1):
        d     = today - timedelta(days=i)
        count = Application.query.filter(
            func.date(Application.submitted_at) == d
        ).count()
        app_trend.append({"date": d.strftime("%b %d"), "count": count})

    return render_template("admin/analytics.html",
                           total_apps=total_apps,
                           total_users=total_users,
                           total_offers=total_offers,
                           total_reject=total_reject,
                           offer_rate=offer_rate,
                           status_data=status_data,
                           role_data=role_data,
                           company_data=company_data,
                           signup_trend=signup_trend,
                           app_trend=app_trend)