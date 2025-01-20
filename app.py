from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash  # Used for password verification
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup (replace with your MongoDB URI)
app.config['MONGO_URI'] = 'mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1'  # MongoDB URI
app.secret_key = 'your_secret_key'  # Set a secret key for session management

mongo = PyMongo(app)

# Route to display the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = mongo.db.users.find_one({'username': username})

        # Check if user exists and if the password matches
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login success
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

# Route to handle the dashboard (for logged-in users)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Create a simple dashboard template


if __name__ == '__main__':
    app.run(debug=True)
