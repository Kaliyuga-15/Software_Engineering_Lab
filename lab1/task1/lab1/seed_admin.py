from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            phone='0000000000',
            password='admin',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='admin', password='admin'")
    else:
        print("Admin already exists.")
