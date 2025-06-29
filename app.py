from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import render_template, redirect, url_for, flash, request
from forms import RegisterForm
# from app import db

db = SQLAlchemy()


#build app
def create_app():
    app = Flask(__name__) #Core
    app.config.from_object(Config) #load settings

    db.init_app(app) #plugging SQLAlchemy into flask

    #Creating tables
    from models import User
    with app.app_context():
        db.create_all()


    #Register
    @app.route("/register", methods = ['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            return render_template("register.html", form = form)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)