from app import create_app, db
from app.models import User, Job, Application, Company
import os

app = create_app(os.environ.get("FLASK_ENV", "development"))

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Job": Job, "Application": Application, "Company": Company}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)