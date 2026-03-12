from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("kitchenbrain.db")

@app.route("/")
def home():
    return "KitchenBrain API Running"

@app.route("/add_food", methods=["POST"])
def add_food():
    data = request.json
    name = data["name"]
    expiry = data["expiry"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO food(name, expiry) VALUES (?,?)", (name, expiry))

    conn.commit()
    conn.close()

    return jsonify({"message":"Food added"})
    
app.run(debug=True)