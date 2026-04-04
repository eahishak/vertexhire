from flask import Blueprint, render_template
from app.models import Job, Company

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    featured_jobs = (Job.query
                     .filter_by(is_active=True)
                     .order_by(Job.created_at.desc())
                     .limit(6).all())

    companies = Company.query.order_by(Company.name).all()

    stats = {
        "jobs":      Job.query.filter_by(is_active=True).count(),
        "companies": Company.query.count(),
    }

    # count per role type for the category section
    all_jobs = Job.query.filter_by(is_active=True).all()
    jobs_by_type = {}
    for j in all_jobs:
        jobs_by_type[j.role_type] = jobs_by_type.get(j.role_type, 0) + 1

    return render_template("home.html",
                           featured_jobs=featured_jobs,
                           companies=companies,
                           stats=stats,
                           jobs_by_type=jobs_by_type)