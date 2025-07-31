from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
from flask_bcrypt import Bcrypt
from mysql.connector.errors import IntegrityError
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
bcrypt = Bcrypt(app)

# MySQL connection
db = mysql.connector.connect(
    user="sqladmin",
    password="uae@123$",
    database="flask_auth",
    host="34.10.221.204",
    port=3306
)
cursor = db.cursor(dictionary=True)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
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
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            flash("Email already exists. Try logging in.", "danger")

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

# Profile edit page (home)
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

        photo_file = request.files.get('photo')
        photo_filename = None

        if photo_file and photo_file.filename != '':
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(UPLOAD_FOLDER, photo_filename))

        if photo_filename:
            sql = "UPDATE users SET email=%s, address=%s, bio=%s, photo=%s WHERE id=%s"
            cursor.execute(sql, (email, address, bio, photo_filename, user_id))
        else:
            sql = "UPDATE users SET email=%s, address=%s, bio=%s WHERE id=%s"
            cursor.execute(sql, (email, address, bio, user_id))

        db.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT email, address, bio, photo FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    return render_template('profile.html', user=user)

# Dashboard page - read-only profile view
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor.execute("SELECT email, address, bio, photo FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template('dashboard.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
