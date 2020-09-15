from flask import Flask, render_template, render_template_string, redirect
from flask_user import login_required
from deplatformr import app


@app.route('/')
@login_required
def homepage():
    return render_template("index.html")


@app.route('/filecoin-files')
@login_required
def filecoin_files():
    return render_template("filecoin/filecoin-files.html")


@app.route('/filecoin-wallets')
@login_required
def filecoin_wallets():
    return render_template("filecoin/filecoin-wallets.html")


@app.route('/filecoin-deals')
@login_required
def filecoin_deals():
    return render_template("filecoin/filecoin-deals.html")


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


@app.route('/instagram')
@login_required
def instagram():
    return render_template("instagram/instagram.html")


@app.route('/icloud')
@login_required
def icloud():
    return render_template("icloud/icloud.html")


@app.route('/google')
@login_required
def google():
    return render_template("google/google.html")
