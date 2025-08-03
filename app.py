from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_bcrypt import Bcrypt

from flask_mail import Mail, Message
import mysql.connector
from mysql.connector.errors import IntegrityError
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os, random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# MySQL connection
db = mysql.connector.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT"))
)
cursor = db.cursor(dictionary=True)


# Upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_otp(email):
    otp = random.randint(100000, 999999)
    session['otp'] = str(otp)
    session['otp_email'] = email

    msg = Message("Your ByteProfiles OTP", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP is {otp}. It is valid for 5 minutes."
    mail.send(msg)
    return otp

@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# -------------------- SIGNUP --------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # OTP Step
        if 'otp' in request.form:
            entered_otp = request.form['otp']
            email = request.form['email']
            if session.get('otp') == entered_otp and session.get('otp_email') == email:
                flash("Signup successful! Please login.", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid OTP. Try again.", "danger")
                return render_template('signup.html', otp_required=True, email=email)

        # Signup Step
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            db.commit()
            send_otp(email)
            flash("OTP sent to your email. Verify to complete signup.", "info")
            return render_template('signup.html', otp_required=True, email=email)
        except IntegrityError:
            flash("Email already exists. Try logging in.", "danger")

    return render_template('signup.html', otp_required=False)

# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # OTP Step
        if 'otp' in request.form:
            entered_otp = request.form['otp']
            email = request.form['email']
            if session.get('otp') == entered_otp and session.get('otp_email') == email:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                if user:
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    flash(f"Welcome back, {user['name']}!", "success")
                    return redirect(url_for('dashboard'))
            flash("Invalid OTP. Try again.", "danger")
            return render_template('login.html', otp_required=True, email=email)

        # Login Step
        email = request.form['email'].strip().lower()
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            send_otp(email)
            flash("OTP sent to your email for verification.", "info")
            return render_template('login.html', otp_required=True, email=email)
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html', otp_required=False)

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        experience = request.form.get('experience', '').strip()
        education = request.form.get('education', '').strip()
        aspiration = request.form.get('aspiration', '').strip()

        cursor.execute("""
            UPDATE users 
            SET experience=%s, education=%s, aspiration=%s
            WHERE id=%s
        """, (experience, education, aspiration, user_id))
        db.commit()
        flash("Profile info updated successfully.", "success")
        return redirect(url_for('dashboard'))

    # GET method - fetch user data and all users
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()

    return render_template('dashboard.html', user=user, all_users=all_users)


# Profile Update
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        address = request.form['address'].strip()
        bio = request.form['bio'].strip()
        skills = request.form.get('skills', '').strip()
        aspiration = request.form.get('aspiration', '').strip()

        # Profile Photo
        photo_file = request.files.get('photo')
        photo_filename = None
        if photo_file and photo_file.filename != '':
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(UPLOAD_FOLDER, photo_filename))

        # CV Upload
        cv_file = request.files.get('cv_file')
        cv_filename = None
        if cv_file and cv_file.filename != '' and allowed_file(cv_file.filename):
            cv_filename = secure_filename(cv_file.filename)
            cv_file.save(os.path.join(UPLOAD_FOLDER, cv_filename))

        # Prepare SQL
        sql = """
            UPDATE users 
            SET email=%s, address=%s, bio=%s, skills=%s, aspiration=%s
        """
        values = [email, address, bio, skills, aspiration]

        if photo_filename:
            sql += ", photo=%s"
            values.append(photo_filename)

        if cv_filename:
            sql += ", cv_file=%s"
            values.append(cv_filename)

        sql += " WHERE id=%s"
        values.append(user_id)

        cursor.execute(sql, tuple(values))
        db.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    return render_template('profile.html', user=user)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
