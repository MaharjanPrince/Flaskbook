from flask import Flask
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user
from extensions import db
from config import Config
from flask import render_template, redirect, url_for, flash, request
from forms import RegisterForm, LoginForm
from models import User




#build app
def create_app():
    app = Flask(__name__) #Core
    app.config.from_object(Config) #load settings

    db.init_app(app) #plugging SQLAlchemy into flask
    login_manager = LoginManager()
    login_manager.login_view = 'login'  # redirect to login page if not logged in
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    

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
    
    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            #scaning user by email
            user = User.query.filter_by(email = form.email.data).first()

            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                #Successful login redirect to home page
                return redirect(url_for('home'))
            else:
                flash("Invalid Email or Incorrect Password", "danger")
                return render_template('login.html', form = form)
            
        #GET request or form validation erros fall here
        return render_template("login.html", form = form)


    
    @app.route("/")
    @login_required
    def home():
        return "<h1>Welcome to FlaskBook!</h1>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)