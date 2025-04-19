"""
Simple Flask-based backend to manage user accounts, subscriptions, 
and license verification requests from the desktop app.
"""

from flask import Flask, request, jsonify
import json
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# For a real deployment, you would use a database like PostgreSQL/MySQL
# or a cloud-based solution. Here, we do a simple JSON file for demo.
DB_FILE = os.path.join(os.path.dirname(__file__), "db.json")

# Utility function to load user data
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({"users": []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Utility function to save user data
def save_db(db_data):
    with open(DB_FILE, 'w') as f:
        json.dump(db_data, f, indent=2)

@app.route("/api/register", methods=["POST"])

def register():
    """
    Endpoint to register a new user. 
    Expects JSON: {"email": "...", "password": "..."}
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    db_data = load_db()
    users = db_data["users"]

    if any(u for u in users if u["email"] == email):
        return jsonify({"message": "User already exists"}), 400

    # Create new user with default subscription expiration of "not subscribed"
    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password,  # For real usage, hash the password (bcrypt, Argon2, etc.)
        "subscription_valid_until": None
    }
    users.append(new_user)
    save_db(db_data)
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    """
    Endpoint to log in a user.
    Expects JSON: {"email": "...", "password": "..."}
    Returns a simple "token" for demonstration. Real apps might return JWT.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    db_data = load_db()
    users = db_data["users"]

    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if user:
        # Return a simple 'session token' for demonstration
        session_token = str(uuid.uuid4())
        return jsonify({"message": "Login successful", "token": session_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    """
    Extend subscription by N days. 
    Expects JSON: {"email":"...", "days": 30}
    """
    data = request.get_json()
    email = data.get("email")
    days = int(data.get("days", 30))

    db_data = load_db()
    users = db_data["users"]

    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    now = datetime.utcnow()
    if user["subscription_valid_until"] is None:
        user["subscription_valid_until"] = (now + timedelta(days=days)).isoformat()
    else:
        subscription_end = datetime.fromisoformat(user["subscription_valid_until"])
        if subscription_end < now:
            # Subscription has expired
            user["subscription_valid_until"] = (now + timedelta(days=days)).isoformat()
        else:
            # Extend from the current expiration date
            user["subscription_valid_until"] = (subscription_end + timedelta(days=days)).isoformat()

    save_db(db_data)
    return jsonify({"message": f"Subscription extended by {days} days."}), 200

@app.route("/api/verify", methods=["GET"])
def verify_subscription():
    """
    Endpoint to verify the subscription status of a user. 
    Expects query param: ?email=...
    Returns JSON with subscription validity.
    """
    email = request.args.get("email")
    if not email:
        return jsonify({"message": "Email parameter required"}), 400

    db_data = load_db()
    users = db_data["users"]

    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if user["subscription_valid_until"] is None:
        return jsonify({"status": "inactive"}), 200
    
    now = datetime.utcnow()
    subscription_end = datetime.fromisoformat(user["subscription_valid_until"])
    if subscription_end > now:
        return jsonify({"status": "active"}), 200
    else:
        return jsonify({"status": "expired"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

@app.route("/", methods=["GET"])
def index():
    return "Hello, CopyAutotyper! The server is up and running.", 200
