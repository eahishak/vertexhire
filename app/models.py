from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(64),  nullable=False)
    last_name     = db.Column(db.String(64),  nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    university    = db.Column(db.String(128))
    major         = db.Column(db.String(128))
    graduation    = db.Column(db.String(20))
    gpa           = db.Column(db.String(10))
    skills        = db.Column(db.Text)          # comma-separated
    github        = db.Column(db.String(200))
    linkedin      = db.Column(db.String(200))
    portfolio     = db.Column(db.String(200))
    bio           = db.Column(db.Text)
    location      = db.Column(db.String(128))
    work_auth     = db.Column(db.String(64))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications  = db.relationship("Application", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    @property
    def profile_strength(self):
        """Returns 0–100 profile completeness score."""
        fields = [self.university, self.major, self.graduation, self.gpa,
                  self.skills, self.github, self.linkedin, self.bio, self.location, self.work_auth]
        filled = sum(1 for f in fields if f and f.strip())
        return int((filled / len(fields)) * 100)

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def __repr__(self):
        return f"<User {self.email}>"


class Company(db.Model):
    __tablename__ = "companies"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(128), nullable=False, unique=True)
    industry     = db.Column(db.String(128), nullable=False)
    location     = db.Column(db.String(128), nullable=False)
    logo_initial = db.Column(db.String(4),   nullable=False)
    color        = db.Column(db.String(10),  default="#635BFF")

    jobs = db.relationship("Job", back_populates="company", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company {self.name}>"


class Job(db.Model):
    __tablename__ = "jobs"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(128), nullable=False)
    role_type   = db.Column(db.String(64),  nullable=False)   # Software Engineering, PM, Data/ML, Design
    company_id  = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    location    = db.Column(db.String(128), nullable=False)
    work_type   = db.Column(db.String(32),  nullable=False)   # Remote, Hybrid, On-site
    experience  = db.Column(db.String(64),  nullable=False)   # Internship, New Grad, Entry Level
    description = db.Column(db.Text,        nullable=False)
    skills      = db.Column(db.Text)                          # comma-separated
    salary_min  = db.Column(db.Integer)
    salary_max  = db.Column(db.Integer)
    deadline    = db.Column(db.String(20))
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    company      = db.relationship("Company", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    @property
    def salary_display(self):
        if not self.salary_min:
            return "Competitive"
        if self.experience == "Internship":
            return f"${self.salary_min:,}–${self.salary_max:,}/mo"
        return f"${self.salary_min:,}–${self.salary_max:,}/yr"

    @property
    def applicant_count(self):
        return self.applications.count()

    def __repr__(self):
        return f"<Job {self.title} @ {self.company.name}>"


APPLICATION_STATUSES = [
    "Submitted", "Under Review", "Screening",
    "Assessment", "Interview", "Final Review",
    "Offer", "Rejected", "Withdrawn"
]

STATUS_COLORS = {
    "Submitted":     "status-blue",
    "Under Review":  "status-blue",
    "Screening":     "status-amber",
    "Assessment":    "status-amber",
    "Interview":     "status-purple",
    "Final Review":  "status-purple",
    "Offer":         "status-green",
    "Rejected":      "status-red",
    "Withdrawn":     "status-gray",
}


class Application(db.Model):
    __tablename__ = "applications"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"),  nullable=False)
    job_id       = db.Column(db.Integer, db.ForeignKey("jobs.id"),   nullable=False)
    status       = db.Column(db.String(32), default="Submitted",     nullable=False)
    cover_note   = db.Column(db.Text)
    # Role-specific answers stored as JSON-like text
    answers      = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="applications")
    job  = db.relationship("Job",  back_populates="applications")

    __table_args__ = (
        db.UniqueConstraint("user_id", "job_id", name="uq_user_job"),
    )

    @property
    def status_color(self):
        return STATUS_COLORS.get(self.status, "status-gray")

    @property
    def stage_index(self):
        stages = ["Submitted", "Under Review", "Screening", "Assessment",
                  "Interview", "Final Review", "Offer"]
        try:
            return stages.index(self.status)
        except ValueError:
            return -1

    def __repr__(self):
        return f"<Application user={self.user_id} job={self.job_id} status={self.status}>"