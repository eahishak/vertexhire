from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, SelectField,
                     SelectMultipleField, BooleanField, SubmitField, HiddenField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.models import User


# ── Auth ────────────────────────────────────────────────────────────────────

class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(1, 64)])
    last_name  = StringField("Last Name",  validators=[DataRequired(), Length(1, 64)])
    email      = StringField("Email",      validators=[DataRequired(), Email(), Length(1, 120)])
    password   = PasswordField("Password", validators=[DataRequired(), Length(8, 128,
                    message="Password must be at least 8 characters.")])
    confirm    = PasswordField("Confirm Password", validators=[DataRequired(),
                    EqualTo("password", message="Passwords must match.")])
    submit     = SubmitField("Create Account")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("An account with this email already exists.")


class LoginForm(FlaskForm):
    email    = StringField("Email",    validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Stay signed in")
    submit   = SubmitField("Sign In")


# ── Profile ──────────────────────────────────────────────────────────────────

WORK_AUTH_CHOICES = [
    ("", "Select…"),
    ("US Citizen", "US Citizen"),
    ("Permanent Resident", "Permanent Resident"),
    ("OPT/CPT", "OPT/CPT"),
    ("H1-B Visa", "H1-B Visa"),
    ("Canadian Citizen", "Canadian Citizen"),
    ("Other", "Other"),
]

class ProfileForm(FlaskForm):
    first_name  = StringField("First Name",  validators=[DataRequired(), Length(1, 64)])
    last_name   = StringField("Last Name",   validators=[DataRequired(), Length(1, 64)])
    university  = StringField("University",  validators=[Optional(), Length(max=128)])
    major       = StringField("Major",       validators=[Optional(), Length(max=128)])
    graduation  = StringField("Expected Graduation (e.g. May 2026)", validators=[Optional(), Length(max=20)])
    gpa         = StringField("GPA",         validators=[Optional(), Length(max=10)])
    location    = StringField("Location",    validators=[Optional(), Length(max=128)])
    work_auth   = SelectField("Work Authorization", choices=WORK_AUTH_CHOICES, validators=[Optional()])
    skills      = StringField("Skills (comma-separated)", validators=[Optional(), Length(max=500)])
    github      = StringField("GitHub URL",    validators=[Optional(), Length(max=200)])
    linkedin    = StringField("LinkedIn URL",  validators=[Optional(), Length(max=200)])
    portfolio   = StringField("Portfolio URL", validators=[Optional(), Length(max=200)])
    bio         = TextAreaField("Bio / Summary", validators=[Optional(), Length(max=1000)])
    submit      = SubmitField("Save Profile")


# ── Application ───────────────────────────────────────────────────────────────

LANG_CHOICES = [
    ("Python", "Python"), ("JavaScript", "JavaScript"), ("TypeScript", "TypeScript"),
    ("Go", "Go"), ("Rust", "Rust"), ("Java", "Java"), ("C++", "C++"), ("C#", "C#"),
    ("Ruby", "Ruby"), ("Swift", "Swift"), ("Kotlin", "Kotlin"), ("Scala", "Scala"),
]

FRAMEWORK_CHOICES = [
    ("React", "React"), ("Next.js", "Next.js"), ("Vue", "Vue"), ("Angular", "Angular"),
    ("Node.js", "Node.js"), ("FastAPI", "FastAPI"), ("Django", "Django"), ("Flask", "Flask"),
    ("Spring Boot", "Spring Boot"), ("Rails", "Rails"), ("Express", "Express"),
]

CLOUD_CHOICES = [
    ("AWS", "AWS"), ("GCP", "GCP"), ("Azure", "Azure"),
    ("Vercel", "Vercel"), ("Cloudflare", "Cloudflare"), ("Supabase", "Supabase"),
]

ML_CHOICES = [
    ("PyTorch", "PyTorch"), ("TensorFlow", "TensorFlow"), ("JAX", "JAX"),
    ("scikit-learn", "scikit-learn"), ("Hugging Face", "Hugging Face"),
    ("LangChain", "LangChain"), ("OpenAI API", "OpenAI API"),
]


class SWEApplicationForm(FlaskForm):
    """Software Engineering application questions."""
    cover_note    = TextAreaField("Cover Note", validators=[Optional(), Length(max=2000)])
    languages     = SelectMultipleField("Programming Languages (select all that apply)",
                        choices=LANG_CHOICES, validators=[Optional()])
    frameworks    = SelectMultipleField("Frameworks & Runtimes",
                        choices=FRAMEWORK_CHOICES, validators=[Optional()])
    cloud         = SelectMultipleField("Cloud / Infra Platforms",
                        choices=CLOUD_CHOICES, validators=[Optional()])
    system_design = SelectField("System Design Experience",
                        choices=[("", "Select…"), ("None yet", "None yet"),
                                 ("Basic concepts", "Basic concepts"),
                                 ("Designed small systems", "Designed small systems"),
                                 ("Designed production systems", "Designed production systems")],
                        validators=[Optional()])
    top_project   = TextAreaField("Describe your most impactful technical project",
                        validators=[Optional(), Length(max=1500)])
    submit        = SubmitField("Submit Application")


class PMApplicationForm(FlaskForm):
    """Product Management application questions."""
    cover_note      = TextAreaField("Cover Note", validators=[Optional(), Length(max=2000)])
    pm_experience   = SelectField("PM / Leadership Experience",
                        choices=[("", "Select…"), ("None", "None"),
                                 ("Club/org leadership", "Club/org leadership"),
                                 ("PM internship", "PM internship"),
                                 ("Full-time PM role", "Full-time PM role")],
                        validators=[Optional()])
    analytics_tools = StringField("Analytics tools you've used (e.g. Mixpanel, Amplitude)",
                        validators=[Optional(), Length(max=300)])
    product_case    = TextAreaField("Product case: How would you improve Notion's onboarding?",
                        validators=[Optional(), Length(max=2000)])
    user_research   = TextAreaField("Describe a time you used user research to inform a decision",
                        validators=[Optional(), Length(max=1500)])
    submit          = SubmitField("Submit Application")


class DataMLApplicationForm(FlaskForm):
    """Data / ML application questions."""
    cover_note   = TextAreaField("Cover Note", validators=[Optional(), Length(max=2000)])
    ml_stack     = SelectMultipleField("ML / Data Libraries",
                        choices=ML_CHOICES, validators=[Optional()])
    sql_level    = SelectField("SQL Proficiency",
                        choices=[("", "Select…"), ("Beginner", "Beginner"),
                                 ("Intermediate", "Intermediate"), ("Advanced", "Advanced"),
                                 ("Expert", "Expert")],
                        validators=[Optional()])
    stats_level  = SelectField("Statistics Background",
                        choices=[("", "Select…"), ("Basic", "Basic"),
                                 ("Intermediate", "Intermediate"), ("Graduate-level", "Graduate-level")],
                        validators=[Optional()])
    ml_project   = TextAreaField("Describe an ML or data project you built end-to-end",
                        validators=[Optional(), Length(max=1500)])
    submit       = SubmitField("Submit Application")


class DesignApplicationForm(FlaskForm):
    """Design application questions."""
    cover_note      = TextAreaField("Cover Note", validators=[Optional(), Length(max=2000)])
    design_tools    = StringField("Design tools (e.g. Figma, Framer, Sketch)",
                        validators=[Optional(), Length(max=300)])
    portfolio_url   = StringField("Portfolio / Case Study URL", validators=[Optional(), Length(max=200)])
    design_process  = TextAreaField("Walk us through your design process on a recent project",
                        validators=[Optional(), Length(max=1500)])
    dev_skills      = SelectField("Frontend / Engineering familiarity",
                        choices=[("", "Select…"), ("None", "None"),
                                 ("Basic HTML/CSS", "Basic HTML/CSS"),
                                 ("React/JS proficient", "React/JS proficient"),
                                 ("Full-stack capable", "Full-stack capable")],
                        validators=[Optional()])
    submit          = SubmitField("Submit Application")


ROLE_FORM_MAP = {
    "Software Engineering": SWEApplicationForm,
    "Product Management":   PMApplicationForm,
    "Data / ML":            DataMLApplicationForm,
    "Design":               DesignApplicationForm,
}

def get_application_form(role_type):
    return ROLE_FORM_MAP.get(role_type, SWEApplicationForm)