from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to continue."
login_manager.login_message_category = "info"

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return app


def _seed_data():
    """Seed sample companies and jobs on first run."""
    from app.models import Company, Job
    if Company.query.first():
        return

    companies = [
        Company(name="Stripe",        industry="Fintech",      location="San Francisco, CA", logo_initial="S", color="#635BFF"),
        Company(name="Notion",        industry="Productivity", location="San Francisco, CA", logo_initial="N", color="#000000"),
        Company(name="Figma",         industry="Design Tools", location="San Francisco, CA", logo_initial="F", color="#F24E1E"),
        Company(name="Vercel",        industry="Cloud / DevOps",location="Remote",           logo_initial="V", color="#000000"),
        Company(name="Anthropic",     industry="AI Research",  location="San Francisco, CA", logo_initial="A", color="#CC785C"),
        Company(name="Linear",        industry="Dev Tools",    location="Remote",            logo_initial="L", color="#5E6AD2"),
    ]
    db.session.add_all(companies)
    db.session.flush()

    jobs = [
        Job(title="Software Engineer Intern",    role_type="Software Engineering",
            company_id=companies[0].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship", deadline="2025-05-01",
            description="Build and scale Stripe's core payment infrastructure. You'll work on APIs used by millions of developers worldwide.",
            skills="Python,Go,PostgreSQL,Redis,REST APIs",
            salary_min=8000, salary_max=10000),
        Job(title="Product Manager Intern",      role_type="Product Management",
            company_id=companies[1].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship", deadline="2025-04-20",
            description="Own product initiatives inside Notion's core editor. Collaborate with design and engineering to ship high-impact features.",
            skills="Product Strategy,User Research,Figma,Analytics,Roadmapping",
            salary_min=7000, salary_max=9000),
        Job(title="Design Engineer",             role_type="Design",
            company_id=companies[2].id, location="San Francisco, CA", work_type="On-site",
            experience="New Grad", deadline="2025-05-15",
            description="Bridge design and engineering at Figma. Build the tools that designers use every day.",
            skills="TypeScript,React,CSS,WebGL,Design Systems",
            salary_min=120000, salary_max=150000),
        Job(title="Frontend Engineer",           role_type="Software Engineering",
            company_id=companies[3].id, location="Remote", work_type="Remote",
            experience="New Grad", deadline="2025-06-01",
            description="Shape the developer experience at Vercel. Work on Next.js, the dashboard, and cutting-edge DX tooling.",
            skills="TypeScript,Next.js,React,Node.js,Tailwind CSS",
            salary_min=130000, salary_max=160000),
        Job(title="Research Engineer Intern",    role_type="Data / ML",
            company_id=companies[4].id, location="San Francisco, CA", work_type="On-site",
            experience="Internship", deadline="2025-04-30",
            description="Work on foundational AI safety research. Contribute to training runs, evals, and interpretability experiments.",
            skills="Python,PyTorch,JAX,Statistics,Machine Learning",
            salary_min=9000, salary_max=12000),
        Job(title="Backend Engineer",            role_type="Software Engineering",
            company_id=companies[5].id, location="Remote", work_type="Remote",
            experience="Entry Level", deadline="2025-05-20",
            description="Build Linear's sync engine and real-time collaboration infrastructure used by top engineering teams.",
            skills="TypeScript,Node.js,PostgreSQL,GraphQL,WebSockets",
            salary_min=140000, salary_max=170000),
    ]
    db.session.add_all(jobs)
    db.session.commit()


def _seed_admin():
    """Create default admin account if it doesn't exist."""
    from app.models import User
    if User.query.filter_by(email="admin@vertexhire.com").first():
        return
    admin = User(
        first_name="Admin",
        last_name="VertexHire",
        email="admin@vertexhire.com",
        is_admin=True,
    )
    admin.set_password("admin1234")
    db.session.add(admin)
    db.session.commit()