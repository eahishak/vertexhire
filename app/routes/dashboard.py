from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models import Application, Job, APPLICATION_STATUSES

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    applications = (current_user.applications
                    .join(Application.job)
                    .order_by(Application.submitted_at.desc())
                    .all())

    status_counts = {}
    for s in APPLICATION_STATUSES:
        status_counts[s] = sum(1 for a in applications if a.status == s)

    active_count    = sum(1 for a in applications if a.status not in ("Offer", "Rejected", "Withdrawn"))
    interview_count = sum(1 for a in applications if a.status == "Interview")
    offer_count     = sum(1 for a in applications if a.status == "Offer")

    applied_ids  = {a.job_id for a in applications}
    recommended  = Job.query.filter(
                       Job.is_active == True,
                       ~Job.id.in_(applied_ids)
                   ).order_by(Job.created_at.desc()).limit(3).all()

    return render_template("dashboard.html",
                           applications=applications,
                           status_counts=status_counts,
                           active_count=active_count,
                           interview_count=interview_count,
                           offer_count=offer_count,
                           recommended=recommended)


@dashboard_bp.route("/withdraw/<int:app_id>", methods=["POST"])
@login_required
def withdraw(app_id):
    application = Application.query.get_or_404(app_id)
    if application.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("dashboard.index"))
    application.status = "Withdrawn"
    db.session.commit()
    flash("Application withdrawn.", "info")
    return redirect(url_for("dashboard.index"))


@dashboard_bp.route("/analytics")
@login_required
def analytics():
    applications = current_user.applications.all()
    total        = len(applications)

    status_counts = {s: 0 for s in APPLICATION_STATUSES}
    for app in applications:
        status_counts[app.status] = status_counts.get(app.status, 0) + 1

    responded      = sum(1 for a in applications if a.status not in ("Submitted", "Withdrawn"))
    response_rate  = round((responded / total * 100), 1) if total else 0

    interviewed    = sum(1 for a in applications if a.status in ("Interview", "Final Review", "Offer"))
    interview_rate = round((interviewed / total * 100), 1) if total else 0

    offers = sum(1 for a in applications if a.status == "Offer")

    role_counts = {}
    for app in applications:
        rt = app.job.role_type
        role_counts[rt] = role_counts.get(rt, 0) + 1

    company_counts = {}
    for app in applications:
        name = app.job.company.name
        company_counts[name] = company_counts.get(name, 0) + 1

    # weekly timeline — last 8 weeks, Windows-safe strftime
    today    = datetime.utcnow().date()
    timeline = []
    for i in range(7, -1, -1):
        week_start = today - timedelta(days=today.weekday() + 7 * i)
        week_end   = week_start + timedelta(days=6)
        count = sum(1 for a in applications
                    if week_start <= a.submitted_at.date() <= week_end)
        # %b %d works on all platforms including Windows
        timeline.append({"label": week_start.strftime("%b %d"), "count": count})

    return render_template("candidate_analytics.html",
                           total=total,
                           response_rate=response_rate,
                           interview_rate=interview_rate,
                           offers=offers,
                           status_counts=status_counts,
                           role_counts=role_counts,
                           company_counts=company_counts,
                           timeline=timeline,
                           applications=applications)