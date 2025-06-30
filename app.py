from flask import Flask
from extensions import db
from config import Config
from flask import render_template, redirect, url_for, flash, request
from forms import RegisterForm




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
            # check for duplicates
            duplicate = User.query.filter(
                (User.username == form.username.data) |
                (User.email == form.email.data)
            ).first()
            if duplicate:
                flash("Username or email already registered", "danger")
                return render_template("register.html", form = form)
            
            #Creating User
            user = User(username = form.username.data,
                        email = form.email.data)
            user.set_password(form.password.data)

            #to Database
            db.session.add(user)
            db.session.commit()

            flash("Registration sucessful!", "sucess")
            return redirect(url_for("home"))
        
#Get or validation erros fall through to here
        return render_template("register.html", form = form)
    
    @app.route("/")
    def home():
        return "<h1>Welcome to FlaskBook!</h1>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)