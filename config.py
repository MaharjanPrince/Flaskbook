import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secre-key") #for form protection, cookies, sessions, etc.
    
    #database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "flaskbook.db")

    #turn off modification tracking(saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False