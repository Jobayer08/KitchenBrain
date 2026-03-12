from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# -------------------------
# Database Connection
# -------------------------
def connect_db():
    return sqlite3.connect("kitchenbrain.db")

# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return "KitchenBrain API Running"

# -------------------------
# Add Food API
# -------------------------
@app.route("/add_food", methods=["POST"])
def add_food():
    data = request.json
    name = data["name"]
    expiry = data["expiry"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO food(name, expiry) VALUES (?,?)",
        (name, expiry)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Food added successfully"})


# -------------------------
# Expiry Checking Function
# -------------------------
def check_expiry():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name, expiry FROM food")

    foods = cur.fetchall()

    alerts = []

    today = datetime.today()

    for food in foods:

        expiry_date = datetime.strptime(food[2], "%Y-%m-%d")

        # expiry 2 দিনের মধ্যে হলে alert
        if expiry_date - today <= timedelta(days=2):

            alerts.append({
                "name": food[1],
                "expiry": food[2]
            })

    conn.close()

    return alerts


# -------------------------
# Expiry Alert API
# -------------------------
@app.route("/check_expiry", methods=["GET"])
def expiry_alert():

    alerts = check_expiry()

    return jsonify(alerts)


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)