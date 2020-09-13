from flask import Flask, render_template, render_template_string, redirect
from flask_user import login_required
from deplatformr import app


@app.route('/')
@login_required
def home_page():
    return render_template("index.html")


@app.route('/members')
@login_required    # User must be authenticated
def member_page():
    # String-based templates
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Members page</h2>
            <p><a href={{ url_for('user.register') }}>Register</a></p>
            <p><a href={{ url_for('user.login') }}>Sign in</a></p>
            <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
            <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
            <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
        {% endblock %}
        """)
