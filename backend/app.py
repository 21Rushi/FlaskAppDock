from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print("Mongo URI:", MONGO_URI)

app = Flask(__name__)

client = MongoClient(MONGO_URI)

print("Mongo Connected DBs:", client.list_database_names())

db = client["FlaskDB"]
collection = db["FlaskDB_collection"]

@app.route("/")
def home():
    return "Welcome to Flask Mongo API"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or request.form

    name = data.get("name")
    email = data.get("email")

    print("Received:", name, email)

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    result = collection.insert_one({
        "name": name,
        "email": email
    })

    print("Inserted ID:", result.inserted_id)

    return jsonify({
        "message": "Data saved in MongoDB",
        "id": str(result.inserted_id),
        "name": name,
        "email": email
    })

if __name__ == "__main__":
    app.run(debug=True)
