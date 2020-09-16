from flask import Flask, render_template
from flask_user import login_required
from deplatformr import app


@app.route('/facebook-deplatform')
@login_required
def facebook_deplatform():
    return render_template("facebook/facebook-deplatform.html")


@app.route('/facebook-upload')
@login_required
def facebook_upload():
    return render_template("facebook/facebook-upload.html")


@app.route('/facebook-view')
@login_required
def facebook_view():
    return render_template("facebook/facebook-view.html")


@app.route('/facebook-manage')
@login_required
def facebook_manage():
    return render_template("facebook/facebook-manage.html")
