from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
import bcrypt

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app)  # Enable CORS for cross-origin requests

# MongoDB Collections
users_collection = mongo.db.users

@app.route("/")
def home():
    return render_template("reg.html")  # Combined HTML page for registration and login

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert user into the database
    users_collection.insert_one({"email": email, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Retrieve the user from the database
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Fetch and verify the stored password
    stored_password = user.get('password', '')

    # Validate stored hash format
    if not stored_password.startswith("$2b$") or len(stored_password) != 60:
        return jsonify({"error": "Invalid password format in the database"}), 500

    # Compare the provided password with the stored hash
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user": {"email": email}}), 200


if __name__ == "__main__":
    app.run(debug=True)
