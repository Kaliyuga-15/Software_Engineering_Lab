import os
from app import create_app
from extensions import db
from models import User


paths = ['electricity.db', 'instance/electricity.db']
for p in paths:
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed {p}")

app = create_app()

with app.app_context():
    db.create_all()

    try:
        db.session.execute(db.text("SELECT employee_id FROM user LIMIT 1"))
        print("Schema check passed: employee_id exists.")
    except Exception as e:
        print(f"Schema check WARNING: {e}")

    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            phone='0000000000',
            password='admin',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin exists.")
