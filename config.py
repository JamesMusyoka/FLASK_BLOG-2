import os

class Config:
 
 
 SECRET_KEY ='SECRET_KEY' or 'you will-never-guess '
 SQLALCHEMY_TRACK_MODIFICATIONS = False
 SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschool:37472377@localhost/flaskblog2'
 UPLOADED_PHOTOS_DEST ='app/static/photos'
 MAIL_SERVER = 'smtp.googlemail.com'
 MAIL_PORT = 587
 MAIL_USE_TLS = True
 MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
 MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
 SIMPLEMDE_JS_IIFE = True
 SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  pass


class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschool:37472377@localhost/flaskblog2_test'

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschool:37472377@localhost/flaskblog2'

  DEBUG = True


config_options = {
'development':DevConfig,
'production':ProdConfig
}

