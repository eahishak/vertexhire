from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # delete existing admin if any
    existing = User.query.filter_by(email="admin@vertexhire.com").first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    admin = User(
        first_name="Admin",
        last_name="VertexHire",
        email="admin@vertexhire.com"
    )
    admin.set_password("admin1234")
    admin.is_admin = True

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully")
    print("Email:   ", admin.email)
    print("is_admin:", admin.is_admin)