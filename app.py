from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Local development only. Set FLASK_SECRET_KEY in your environment.
app.secret_key = os.environ["FLASK_SECRET_KEY"]

# Fictional users for the educational demo
users = {
    "alice": {
        "id": 1,
        "password_hash": generate_password_hash("alice-demo-password")
    },
    "bob": {
        "id": 2,
        "password_hash": generate_password_hash("bob-demo-password")
    }
}

invoices = {
    101: {"id": 101, "owner_id": 1, "customer": "Alice", "amount": 250},
    102: {"id": 102, "owner_id": 2, "customer": "Bob", "amount": 700}
}

@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if not user or not isinstance(password, str) or not check_password_hash(
        user["password_hash"], password
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    session.clear()
    session["user_id"] = user["id"]

    return jsonify({"message": "Login successful"}), 200


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@app.get("/api/invoices/<int:invoice_id>")
def get_invoice(invoice_id):

    # Step 1: Verify that the user is logged in
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Authentication required"}), 401

    # Step 2: Find the invoice
    invoice = invoices.get(invoice_id)

    if invoice is None:
        return jsonify({"error": "Invoice not found"}), 404

    # Step 3: Verify ownership
    if invoice["owner_id"] != user_id:
        return jsonify({"error": "Access denied"}), 403

    # Step 4: Return the authorized invoice
    return jsonify(invoice), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)