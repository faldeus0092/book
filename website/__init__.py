from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    # secure cookies
    app.config['SECRET_KEY'] = 'verysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/book'
    db.init_app(app)

    # register the view
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(views, url_prefix='/upload')
    return app