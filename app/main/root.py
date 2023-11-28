from flask import render_template, send_from_directory

from models import Dice

from . import main


##
## Main
##
@main.route("/")
def root():
    return render_template("main/main.html")


@main.route("/ss13")
def main_ss13():
    return render_template("main/ss13.html")


@main.route("/ss13/rules")
def main_ss13_rules():
    return render_template("main/rules.html")


##
## Dice
##
@main.route("/dice")
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


#
# Other
#
@main.route("/robots.txt", methods=["GET"])
def robots():
    return send_from_directory("static", "robots.txt")


@main.route("/sitemap.xml", methods=["GET"])
def sitemap():
    return send_from_directory("static", "sitemap.xml")
