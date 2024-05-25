from flask import Flask, redirect, request, render_template, url_for, flash, jsonify
from model import validate_urls, process_data, user_input_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = 'SUPER_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

# Create the database


def create_tables():
    with app.app_context():
        try:
            db.create_all()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# for handling 404 not found error


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_404.html'), 404

# for handling 500 internal server error


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error_505.html'), 500

# login user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# signup user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            hashed_password = generate_password_hash(
                password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

# logout user


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# route to get urls


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        url1 = request.form['url1']
        url2 = request.form['url2']
        url3 = request.form['url3']
        slider_value = request.form['slider']
        urls = validate_urls(url1, url2, url3)

        if isinstance(urls, list):
            process_data(urls, slider_value)
            return redirect(url_for('process'))
        else:
            flash(urls, 'danger')
            return render_template('index.html')
    else:
        return render_template('index.html')

# route for question answering


@app.route('/process', methods=['GET', 'POST'])
@login_required
def process():
    if request.method == 'POST':
        question = request.json['question']
        answer = user_input_response(question)
        answer = answer['output_text']
        return jsonify({'answer': answer})

    return render_template("process.html")


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
