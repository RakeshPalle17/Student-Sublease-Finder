from app import create_app, db
from app.models import User, Listing
from app.routes import main
from app.auth import auth

app = create_app()
app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
