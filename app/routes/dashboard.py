from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
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

    # Recommended jobs = jobs not yet applied to
    applied_ids     = {a.job_id for a in applications}
    recommended     = Job.query.filter(
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