from extensions import db
from models import User

def seed_admin():
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
