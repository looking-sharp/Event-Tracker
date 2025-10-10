from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv # type: ignore
from flask import Flask, request, redirect, url_for, render_template, jsonify # type: ignore
from datetime import datetime
import uuid
import os

load_dotenv()
uri = os.getenv("DATABASE_URL")
client = MongoClient(uri)
db = client.event_tracker

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

def format_time(time_str):
    return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/signUp", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = uuid.uuid4().hex[:8]
        # while unlikely, don't want more than one user to have same id
        while db.users.find_one({"_id":user_id}):
            user_id = uuid.uuid4().hex[:8]
        db.users.insert_one({
            "_id": user_id,
            "username": username,
            "password": password
        })
        return redirect(url_for("user_page", user_id=user_id))
    return render_template("signUp.html")

@app.route("/check_username")
def check_username():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"exists": False})

    exists = db.users.find_one({"username": username}) is not None
    return jsonify({"exists": exists})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.users.find_one({"username": username, "password":password})
        print(user)
        if user == None:
            return render_template("login.html", login_failed=True)
        return redirect(url_for("user_page", user_id=user["_id"]))
    return render_template("login.html")

@app.route("/userHome/<user_id>")
def user_page(user_id):
    user = db.users.find_one({"_id":user_id})
    if user == None:
        # user needs to log in first
        return render_template("signUp.html")
    events = db.events.find({"user_id":user_id})
    return render_template("userHome.html", username=user["username"], user_id=user_id, events=events)
    
@app.route("/createEvent/<user_id>", methods=["GET", "POST"])
def create_event(user_id):
    if request.method == "POST":
        event_name = request.form["eventName"]
        event_date = request.form["eventDate"]
        event_location = request.form["location"]
        event_description = request.form["description"]
        start_time = format_time(request.form["startTime"])
        end_time = format_time(request.form["endTime"])
        public = request.form["public"]
        event_id = uuid.uuid4().hex[:8]
        while db.events.find_one({"_id":event_id}):
            event_id = uuid.uuid4().hex[:8]
        db.events.insert_one({
            "_id": event_id,
            "user_id": user_id,
            "eventName": event_name,
            "eventDate": event_date,
            "startTime": start_time,
            "endTime": end_time,
            "public": public,
            "eventLocation": event_location,
            "eventDescription": event_description,
            "rsvps":[]
        })
        return redirect(url_for("user_page", user_id=user_id))
    return render_template("newEvent.html", user_id=user_id)

@app.route("/rsvp/<event_id>", methods=["GET", "POST"])
def rsvp(event_id):
    event = db.events.find_one({"_id": event_id})
    if not event:
        return "Event not found", 404
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        rsvp_entry = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
        }
        db.events.update_one(
            {"_id": event_id},
            {"$addToSet": {"rsvps": rsvp_entry}}
        )
        return "Thanks for RSVPing!"
    return render_template("rsvpForm.html", event=event)

@app.route("/delete_event/<event_id>/<user_id>", methods=["POST"])
def delete_event(event_id, user_id):
    result = db.events.delete_one({"_id": event_id, "user_id": user_id})
    if result.deleted_count == 0:
        return "Event not found or you don't have permission", 404
    return redirect(url_for("user_page", user_id=user_id))

if __name__ == "__main__":
    app.run(debug=True)