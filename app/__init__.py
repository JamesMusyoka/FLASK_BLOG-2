from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from config import DevConfig


photos = UploadSet('photos',IMAGES)
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
simple = SimpleMDE()
   # migrate = Migrate(app, db)

def create_app(config_name):
   app = Flask(__name__)

   app.config.from_object(config_options[config_name])

   bootstrap.init_app(app)
   db.init_app(app)
   login_manager.init_app(app)
   simple.init_app(app)
   mail.init_app(app)

   from .main import main as main_blueprint
   app.register_blueprint(main_blueprint)
   
   configure_uploads(app,photos)

   return app
