from flask_socketio import SocketIO
from flask import Flask, jsonify, render_template, request, send_from_directory
from database import db_session
from models import Dice
import json

with open("config.json") as config:
    conf = json.loads(config.read())

app = Flask(__name__)
app.config["SECRET_KEY"] = conf["secret_key"]
socketio = SocketIO(app)


##
## Main
##
@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("main/main.html")


@app.route("/ss13", methods=["GET", "POST"])
def main_ss13():
    return render_template("main/ss13.html")


@app.route("/ss13/rules", methods=["GET", "POST"])
def main_ss13_rules():
    return render_template("main/rules.html")


#
# Errors
#
@app.errorhandler(400)
def bad_request(error):
    return render_template("error/400.html")


@app.errorhandler(401)
def unauthorized(error):
    return render_template("error/401.html")


@app.errorhandler(403)
def forbidden(error):
    return render_template("error/403.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("error/404.html")


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html")


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


@app.route("/api/insert_dice_roll", methods=["POST"])
def insert_dice_roll():
    try:
        data = request.get_json()

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
    socketio.run(app, debug=False)
