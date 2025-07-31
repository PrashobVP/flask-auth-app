from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")

db = mysql.connector.connect(
    user=db_user,
    password=db_pass,
    database=db_name,
    unix_socket=f"/cloudsql/{instance_connection_name}"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return redirect('/login')

# ----------------- SIGN UP -----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            db.commit()
            return redirect('/login')
        except:
            return "Email already exists!"

    return render_template('signup.html')

# ----------------- LOGIN -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            return f"Welcome {user['name']}! Login Successful."
        else:
            return "Invalid credentials!"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
