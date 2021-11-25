from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from app.routes import user, transaction, categories
from app.model.model import db
from app.ma import ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/pda"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
bcrypt = Bcrypt(app)


with app.app_context():
    db.create_all()
    db.session.commit()
    migrate = Migrate(app, db)
    app.register_blueprint(user.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(categories.bp)

@app.route('/hello')
def hello():
    return "Hello, World!"
