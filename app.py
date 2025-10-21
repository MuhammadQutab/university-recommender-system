import random
from future_prediction import get_future_career_options
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField
from wtforms.validators import InputRequired, Length, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
import future_prediction
import pickle
import pandas as pd
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


model_file_path = 'final_model.pkl'
model_loaded = False
model_error = ""
all_departments = ['Law', 'Islamic Studies','Education', 'Computer Science and Information Technology', 'Artificial Intelligence', 'Data Science', 'Business Administration', 'Public Administration', 'Accounting and Finance','Biotechnology', 'Botany', 'Business Administration', 'Computer Science', 'Economics', 'Education', 'International Relations', 'Mathematics', 'Psychology', 'Statistics', 'Urdu', 'Zoology','Public Health', 'English', 'Sociology', 'Islamic Economy and Banking', 'Mass Communication', 'Department of International Relations', 'Department of Psychology', 'Management Sciences', 'Department of Urdu', 'Sociology & Rural Development', 'Department of Law', 'Institute Of Languages', 'Institute of Kashmir Studies', 'Department of English', 'Institute Of Education', 'Kashmir Institute of Economics', 'Art and Design', 'Related Posts',
                    'Health and Medical Sciences', 'Faculty of Engineering', 'Physiotherapy', 'Public Health', 'BS Allied Health Sciences', 'Botany', 'Computer Science & Information Technology', 'Department of Biotechnology', 'Geology', 'Physics', 'Department of Electrical Engineering', 'Department of Software Engineering', 'Department of Software Engineering Events','Biotechnology']

try:
    if os.path.exists(model_file_path):
        with open(model_file_path, 'rb') as model_file:
            model = pickle.load(model_file)
        model_loaded = True
        print("Model loaded successfully.")
    else:
        model_error = f"Model file {model_file_path} not found."
except Exception as e:
    print(f"An Error Occured: {e}")
    model_error = str(e)

# Define User model


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
                        InputRequired(), Email(), Length(min=6, max=30)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=5, max=80)])


class PredictionForm(FlaskForm):
    admission_marks = FloatField(
        'HSSC Marks (%)', id='admission_marks', validators=[InputRequired()])
    minimum_entry_mark = FloatField(
        'SSC Marks (%)', id='minimum_entry_mark', validators=[InputRequired()])
    fees_structure = FloatField(
        'Affordable Fee', id='fees_structure', validators=[InputRequired()])
    departments_offered = StringField(
        'Your Interest', id='departments_offered', validators=[InputRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists in the database
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()

        if existing_user:
            # Return a message if the user exists
            if existing_user.username == username:
                error_message = "Username already taken."
            elif existing_user.email == email:
                error_message = "Email already registered."
            return render_template('signup.html', error=error_message)

        # Proceed with user registration if username and email are unique
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            login_user(user)
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    prediction_result = False
    form = PredictionForm()
    if form.validate_on_submit():
        if not model_loaded:
            flash('Model is not loaded', 'danger')
        else:
            try:
                data = {
                    "Admission_marks": form.admission_marks.data,
                    "Minimum_entry_mark": form.minimum_entry_mark.data,
                    "Fees_structure": form.fees_structure.data,
                    "Departments_Offered": form.departments_offered.data
                }

                df = pd.DataFrame([data])
                expected_columns = [
                    'Admission_marks', 'Minimum_entry_mark', 'Fees_structure', 'Departments_Offered']
                if not all(col in df.columns for col in expected_columns):
                    flash('Data format mismatch', 'danger')
                    return render_template('dashboard.html', name=current_user.username, form=form)

                prediction = model.predict(df)
                flash(f'Prediction: {prediction[0]}', 'success')
                prediction_result = True

            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')

    return render_template('dashboard.html', name=current_user.username, form=form, departments=all_departments, universities=universities)


@app.route('/check_model', methods=['GET'])
def check_model():
    if model_loaded:
        return jsonify({'status': 'Model loaded successfully'})
    else:
        return jsonify({'error': f'Model failed to load: {model_error}'}), 500


universities = {
    'Quaid-i-Azam University': 1,
    'COMSATS University Islamabad': 2,
    'National University of Sciences and Technology': 3,
    'University of the Punjab': 4,
    'University of Engineering and Technology, Lahore': 5,
    'University of Peshawar': 6,
    'Government College University Faisalabad': 7,
    'The University of Lahore': 8,
    'Lahore university of Management Science (LUMS)': 9,
    'University of Agriculture Faisalabad': 10,
    'Bahauddin Zakariya University': 11,
    'International Islamic University Islamabad': 12,
    'The Aga Khan University': 13,
    'Abdul Wali Khan University Mardan': 14,
    'PMAS Arid Agriculture University Rawalpindi': 15,
    'University of Azad Jammu & Kashmir': 68,
    'WOMEN UNIVERSITY AZAD JAMMU & KASHMIR (WU) BAGH DEGREES': 172,
    'Unversity Of The Poonch, Rawala Kot Rawalakot': 138,
    'University Of Kotli AJ&K': 165,
    'Mirpur University Of Science And Technology Mir Pur (ajk)': 90,
    'Mohi-ud-din Islamic University, Mir Pur (ajk)': 161
}


universities_reverse = {v: k for k, v in universities.items()}


@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model is not loaded'}), 500
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        print("DataFrame:\n", df)

        department_offered = df.loc[0, 'Departments_Offered']

        careers = get_future_career_options(department_offered)
        print(f"Careers in: {department_offered}: {careers}")

        prediction = model.predict(df)
        predicted_index = int(prediction[0])

        predicted_university = universities_reverse.get(
            predicted_index, 'Unknown University')

        all_universities = list(universities.keys())
        all_universities.remove(predicted_university)
        random_universities = random.sample(all_universities, 2)
        selected_universities = [predicted_university] + random_universities

        return jsonify({
            'university': selected_universities,
            'Department': department_offered,
            'careers': careers
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
