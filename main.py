import re
from flask_socketio import SocketIO
from flask import Flask, jsonify, render_template, request, send_from_directory
from sqlalchemy import inspect
from database import db_session
from models import Dice
import json
from modules import Validate

with open("config.json") as config:
    conf = json.loads(config.read())

app = Flask(__name__)
app.config["SECRET_KEY"] = conf["secret_key"]
socketio = SocketIO(
    app,
    cors_allowed_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://nukeops.com",
    ],
)


##
## Main
##
@app.route("/")
def main():
    return render_template("main/main.html")


@app.route("/ss13")
def main_ss13():
    return render_template("main/ss13.html")


@app.route("/ss13/rules")
def main_ss13_rules():
    return render_template("main/rules.html")


#
# Errors
#
@app.errorhandler(Exception)
def handle_error(error):
    error = getattr(error, "code", 500)
    if error == 400:
        return render_template("error.html", error_code=f"{error} - BAD REQUEST")
    elif error == 401:
        return render_template("error.html", error_code=f"{error} - AUTH REQUIRED")
    elif error == 403:
        return render_template("error.html", error_code=f"{error} - PAGE FORBIDDEN")
    elif error == 404:
        return render_template("error.html", error_code=f"{error} - PAGE NOT FOUND")

    return render_template("error.html", error_code=f"{error} - UNKNOWN ERROR")


##
## Dice
##
@app.route("/dice")
def dice():
    fetch_dice_records = Dice.query.order_by(Dice.date.desc()).limit(10).all()
    dice_records = [
        {
            "name": record.name,
            "dice": record.dice,
            "sides": record.sides,
            "throws": record.throws,
            "sum": record.sum,
            "modifier": record.modifier,
            "date": record.date.strftime("%d/%m/%Y \n%H:%M:%S"),
        }
        for record in fetch_dice_records
    ]

    return render_template("dice/dice.html", dice_records=dice_records)


def valid_dice(data) -> bool:
    try:
        for key, value in data.items():
            print(key, value, type(value))
            # check if ints are ints
            if key in ["dice", "sides", "sum"] and type(value) != int:
                return False

            if type(value) == str:
                # check the pattern "{mod}({+/-}{number})"
                if key == "modifier":
                    if (
                        not re.match(r"^(str|int|dex|con|wis|cha)\([+-]\d+\)$", value)
                        and value != ""
                    ):
                        return False

                # pass only numbers and ,
                if key == "throws":
                    if not re.match(r"^[0-9, ]+$", value):
                        return False

                # pass only alphanumeric
                if not re.match(r"^[0-9a-zA-Z,+\- ]+$", value) and key not in [
                    "modifier",
                    "throws",
                ]:
                    return False
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@app.route("/api/insert_dice_roll", methods=["POST"])
def insert_dice_roll():
    try:
        data = request.get_json()

        if not valid_dice(data):
            return jsonify({"error": "Invalid dice data"}), 500

        new_dice_roll = Dice(
            name=data.get("name"),
            dice=data.get("dice"),
            sides=data.get("sides"),
            throws=data.get("throws"),
            sum=data.get("sum"),
            modifier=data.get("modifier"),
        )

        db_session.add(new_dice_roll)
        db_session.commit()
        socketio.emit("dice_table_update")
        return jsonify({"message": "Dice roll recorded successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/api/get_dice_rolls", methods=["GET"])
def get_dice_rolls():
    try:
        dice_records = Dice.query.order_by(Dice.date.desc()).limit(10).all()
        dice_records_json = [
            {
                "name": record.name,
                "dice": record.dice,
                "sides": record.sides,
                "throws": record.throws,
                "sum": record.sum,
                "modifier": record.modifier,
                "date": record.date.strftime("%d/%m/%Y \n%H:%M:%S"),
            }
            for record in dice_records
        ]
        return jsonify(dice_records_json)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


#
# Other
#
@app.route("/robots.txt", methods=["GET"])
def robots():
    return send_from_directory("static", "robots.txt")


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    return send_from_directory("static", "sitemap.xml")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)
