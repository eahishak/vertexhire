# VertexHire

A full-stack candidate hiring portal built with Flask. Candidates discover jobs, build profiles, submit role-adaptive applications, and track their hiring pipeline. Admins manage candidates, move applications through stages, and view platform analytics.

---

## Setup

```bash
pip install -r requirements.txt
python run.py
```

App runs at `http://127.0.0.1:5000`

Database, companies, jobs, and admin account are created automatically on first run.

---

## Admin Login

```
Email:    admin@vertexhire.com
Password: admin1234
```

If the admin account is missing: `python create_admin.py`

---

## URLs

| URL | Description |
|-----|-------------|
| `/` | Home |
| `/jobs/` | Browse and search jobs |
| `/jobs/<id>` | Job detail |
| `/jobs/<id>/apply` | Apply — role-adaptive form |
| `/auth/register` | Create account |
| `/auth/login` | Sign in |
| `/auth/profile` | Edit profile |
| `/dashboard/` | Candidate dashboard |
| `/dashboard/analytics` | Candidate analytics |
| `/admin/` | Admin overview |
| `/admin/applications` | All applications |
| `/admin/candidates` | All candidates |
| `/admin/analytics` | Platform analytics |

---

## Database

**users** — candidate accounts and profiles
- `id` PK, `first_name`, `last_name`, `email` (unique), `password_hash`, `is_admin`, `university`, `major`, `graduation`, `gpa`, `skills`, `github`, `linkedin`, `portfolio`, `bio`, `location`, `work_auth`, `created_at`, `updated_at`

**companies** — seeded company data
- `id` PK, `name` (unique), `industry`, `location`, `logo_initial`, `color`

**jobs** — job listings
- `id` PK, `title`, `role_type`, `company_id` FK → companies, `location`, `work_type`, `experience`, `description`, `skills`, `salary_min`, `salary_max`, `deadline`, `is_active`, `created_at`

**applications** — candidate applications
- `id` PK, `user_id` FK → users, `job_id` FK → jobs, `status`, `cover_note`, `answers`, `submitted_at`, `updated_at`
- Unique constraint on `(user_id, job_id)`

---

## Forms (WTForms)

- `RegistrationForm` — inserts User at `/auth/register`
- `LoginForm` — authenticates at `/auth/login`
- `ProfileForm` — updates User at `/auth/profile`
- `SWEApplicationForm` — inserts Application for Software Engineering roles
- `PMApplicationForm` — inserts Application for Product Management roles
- `DataMLApplicationForm` — inserts Application for Data / ML roles
- `DesignApplicationForm` — inserts Application for Design roles

All forms redirect on success (PRG pattern).

---

## Stack

- Python 3.12, Flask 3.x
- Flask-SQLAlchemy (SQLite)
- Flask-Login, Flask-WTF, WTForms, Werkzeug
- Jinja2, vanilla CSS, Chart.js