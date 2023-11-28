import re

from flask import Blueprint, jsonify, request

from database import db_session
from models import Dice

from .. import socketio
from . import main


##
## Dice
##
def valid_dice(data) -> bool:
    try:
        for key, value in data.items():
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


@main.route("/api/insert_dice_roll", methods=["POST"])
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
        return (
            jsonify(
                {
                    "message": "Dice roll recorded successfully",
                    "timestamp": new_dice_roll.date.strftime("%d/%m/%Y %H:%M:%S"),
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@main.route("/api/get_dice_rolls", methods=["GET"])
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
