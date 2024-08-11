from flask import Flask, render_template, redirect, url_for, flash, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from config import Config
from models import db, User, Brief
from brief_generator import generate_brief
from datetime import datetime, timedelta
import pytz



app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'salman_faizi'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

def render_generator():
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
    
    return render_template('index.html', content=content)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/')
# def index():
#     return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('introduction.html')

# @app.route('/login_redirect')
# def login_redirect():
#     return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            flash('Username or Email already exists! Please try logging in or use a different username/email.', 'warning')
            return redirect(url_for('signup'))
        
        # Create new user if no conflict
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = authenticate_user(email, password)
        
        if user:
            login_user(user)
            # render_generator

            return redirect(url_for('home'))  # Redirect to the dashboard or another page
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

    
    # return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('start_time', None)  # Clear guest session data
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
            brief = Brief(type=brief_type, domain=domain, content=content, author=current_user)
            db.session.add(brief)
            db.session.commit()
    return render_template('index.html', content=content)



@app.route('/guest_home', methods=['GET', 'POST'])
def guest_home():
    # Initialize session start time if not set
    if 'start_time' not in session:
        session['start_time'] = datetime.utcnow().isoformat()
    
    start_time_str = session.get('start_time')
    start_time = datetime.fromisoformat(start_time_str)
    
    # Check if 30 minutes have passed
    time_elapsed = datetime.utcnow() - start_time
    
    if time_elapsed > timedelta(minutes=30):
        # Session expired, either redirect to session_expired page
        session.pop('start_time', None)  # Clear session start time
        flash("Your guest session has expired. Please sign up to continue.", "warning")
        return redirect(url_for('session_expired'))  # Redirect to session_expired page
    
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
    
    return render_template('index.html', content=content)




@app.route('/session_expired')
def session_expired():
    return render_template('session_expired.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
