from flask import render_template


def page_not_found(error):
    return render_template("generic/404.html"), 404


def internal_error(error):
    return render_template("generic/500.html"), 500


def forbidden_error(error):
    return render_template("generic/403.html"), 403
