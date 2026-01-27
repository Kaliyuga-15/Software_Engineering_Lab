from flask import Flask, session, g
from extensions import db
from models import User
from seed_admin import seed_admin

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'simple-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///electricity.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.employee import employee_bp
    from routes.consumer import consumer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(consumer_bp)

    @app.before_request
    def load_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    @app.context_processor
    def inject_user():
        return dict(user=g.user)

    with app.app_context():
        db.create_all()
        seed_admin()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
