from flask import Blueprint, render_template, request
from app.models import Job, Company

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    featured_jobs = (Job.query
                     .filter_by(is_active=True)
                     .order_by(Job.created_at.desc())
                     .limit(6).all())
    companies = Company.query.all()
    stats = {
        "jobs":      Job.query.filter_by(is_active=True).count(),
        "companies": Company.query.count(),
    }
    return render_template("home.html", featured_jobs=featured_jobs,
                           companies=companies, stats=stats)