from flask import render_template

from . import main


@main.app_errorhandler(Exception)
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


@main.route("/test")
def test():
    return render_template("error.html")
