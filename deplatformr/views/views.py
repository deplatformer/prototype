from flask import Flask, render_template, render_template_string, redirect
from flask_user import login_required
from deplatformr import app


@app.route('/')
@login_required
def homepage():
    return render_template("homepage.html")


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
