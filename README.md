# VertexHire — Intelligent Student Hiring Infrastructure

## Purpose
VertexHire is a full student hiring portal where students can discover job opportunities from top companies, build a persistent profile, submit role-adaptive applications, and track every stage of their hiring pipeline from submission through offer — all in one place.

---

## How to Run

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python run.py
```

The app will start at **http://127.0.0.1:5000**

The SQLite database (`vertexhire.db`) is created automatically on first run, along with seed data (6 companies, 6 jobs).

---

## Navigation

| URL | Page |
|-----|------|
| `/` | Home — hero, featured jobs, company logos, how it works |
| `/jobs/` | Browse all jobs — search + filter by role, work type, experience |
| `/jobs/<id>` | Job detail — full description, skills, apply button |
| `/jobs/<id>/apply` | Role-adaptive application form (different questions per role type) |
| `/auth/register` | Create account |
| `/auth/login` | Sign in |
| `/auth/logout` | Sign out |
| `/auth/profile` | Edit student profile (inserts/updates the `users` table) |
| `/dashboard/` | Student dashboard — stats, application tracker with pipeline, recommended jobs |
| `/dashboard/withdraw/<id>` | Withdraw an application (POST) |

---

## Database Tables

### `users`
Stores student accounts and profile data.

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| first_name | String(64) | Required |
| last_name | String(64) | Required |
| email | String(120) | Unique, required |
| password_hash | String(256) | Hashed via Werkzeug |
| university | String(128) | Optional |
| major | String(128) | Optional |
| graduation | String(20) | Optional |
| gpa | String(10) | Optional |
| skills | Text | Comma-separated |
| github | String(200) | Optional |
| linkedin | String(200) | Optional |
| portfolio | String(200) | Optional |
| bio | Text | Optional |
| location | String(128) | Optional |
| work_auth | String(64) | Optional |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

### `companies`
Stores company data (seeded on first run).

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| name | String(128) | Unique |
| industry | String(128) | Required |
| location | String(128) | Required |
| logo_initial | String(4) | Display letter |
| color | String(10) | Hex color for logo |

### `jobs`
Stores job listings. **Foreign key → companies.id**

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| title | String(128) | Required |
| role_type | String(64) | Drives form selection |
| company_id | Integer | **FK → companies.id** |
| location | String(128) | Required |
| work_type | String(32) | Remote / Hybrid / On-site |
| experience | String(64) | Internship / New Grad / Entry Level |
| description | Text | Required |
| skills | Text | Comma-separated |
| salary_min | Integer | Optional |
| salary_max | Integer | Optional |
| deadline | String(20) | Optional |
| is_active | Boolean | Default True |
| created_at | DateTime | Auto |

### `applications`
Tracks student applications. **Foreign keys → users.id and jobs.id**

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| user_id | Integer | **FK → users.id** |
| job_id | Integer | **FK → jobs.id** |
| status | String(32) | Pipeline stage |
| cover_note | Text | Optional |
| answers | Text | JSON-encoded role answers |
| submitted_at | DateTime | Auto |
| updated_at | DateTime | Auto |

Unique constraint on `(user_id, job_id)` — one application per student per job.

---

## WTForms Usage
- `RegistrationForm` — `/auth/register` — inserts a new `User`
- `LoginForm` — `/auth/login`
- `ProfileForm` — `/auth/profile` — updates `User` (insertion on first save)
- `SWEApplicationForm` — `/jobs/<id>/apply` for Software Engineering roles — inserts `Application`
- `PMApplicationForm` — same route for Product Management roles
- `DataMLApplicationForm` — same route for Data/ML roles
- `DesignApplicationForm` — same route for Design roles

All POST forms redirect on success (PRG pattern).

---

## Technologies Used
- Python 3.10+, Flask 3.x
- Flask-SQLAlchemy (SQLite)
- Flask-Login (session auth)
- Flask-WTF + WTForms (forms + CSRF)
- Werkzeug (password hashing)
- Jinja2 (templating)
- Vanilla CSS (custom design system, fully responsive)
- Inter font (Google Fonts)