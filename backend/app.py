from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

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
# Get All Foods
# -------------------------
@app.route("/foods", methods=["GET"])
def get_foods():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM food")
    foods = cur.fetchall()

    conn.close()

    food_list = []

    for f in foods:

        food_list.append({
            "id": f[0],
            "name": f[1],
            "expiry": f[2]
        })

    return jsonify(food_list)


# -------------------------
# Delete Food
# -------------------------
@app.route("/delete_food/<int:id>", methods=["DELETE"])
def delete_food(id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM food WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Food deleted"})


# ----------------------------------
# AI Recipe Generator (Rule Based)
# ----------------------------------
@app.route("/ai_recipes", methods=["GET"])
def ai_recipes():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT name FROM food")
    foods = cur.fetchall()

    conn.close()

    ingredients = [f[0].lower() for f in foods]

    if len(ingredients) == 0:
        return jsonify({"recipes": ["No ingredients found in fridge."]})

    recipes = []

    # Rule Based Recipes
    if "egg" in ingredients and "tomato" in ingredients:
        recipes.append("Tomato Omelette")

    if "chicken" in ingredients and "tomato" in ingredients:
        recipes.append("Chicken Tomato Curry")

    if "milk" in ingredients and "egg" in ingredients:
        recipes.append("Pancake")

    if "potato" in ingredients:
        recipes.append("Potato Fry")

    if "rice" in ingredients and "egg" in ingredients:
        recipes.append("Egg Fried Rice")

    if "chicken" in ingredients:
        recipes.append("Grilled Chicken")

    # Default Recipe
    if len(recipes) == 0:
        recipes.append("Simple Mixed Vegetable Fry")

    return jsonify({"recipes": recipes})


# -------------------------
# AI Meal Planner
# -------------------------
@app.route("/meal_plan", methods=["GET"])
def meal_plan():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT name FROM food")
    foods = cur.fetchall()

    conn.close()

    ingredients = [f[0].lower() for f in foods]

    if len(ingredients) == 0:
        return jsonify({"message": "No ingredients found in fridge."})

    breakfast = "Bread and Tea"
    lunch = "Simple Rice Meal"
    dinner = "Vegetable Fry"

    # Breakfast rules
    if "egg" in ingredients and "milk" in ingredients:
        breakfast = "Pancake"
    elif "egg" in ingredients:
        breakfast = "Boiled Egg with Bread"

    # Lunch rules
    if "chicken" in ingredients and "rice" in ingredients:
        lunch = "Chicken Curry with Rice"
    elif "rice" in ingredients and "egg" in ingredients:
        lunch = "Egg Fried Rice"

    # Dinner rules
    if "tomato" in ingredients and "egg" in ingredients:
        dinner = "Tomato Omelette"
    elif "chicken" in ingredients:
        dinner = "Grilled Chicken"

    meal = {
        "Breakfast": breakfast,
        "Lunch": lunch,
        "Dinner": dinner
    }

    return jsonify(meal)


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
