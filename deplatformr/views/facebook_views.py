import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from flask_user import login_required, current_user
from deplatformr import app, db
from deplatformr.helpers.helpers import unzip
from deplatformr.helpers.facebook_helpers import posts_to_db


@app.route('/facebook-deplatform')
@login_required
def facebook_deplatform():
    return render_template("facebook/facebook-deplatform.html", breadcrumb="Facebook / Deplatform")


@app.route('/facebook-upload', methods=["GET", "POST"])
@login_required
def facebook_upload():

    # Assume upload didn't happen or failed until proven otherwise
    upload_success = False

    # Uploading a new file
    if request.method == "POST":

        # Get the filename from the request
        upload = request.files['uploadfile']

        # Use the default upload directory configured for the app
        upload_path = app.config["UPLOADDIR"]
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Create a subdirectory per username. Usernames are unique.
        user_dir = os.path.join(upload_path, current_user.username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        # Create a Facebook subdirectory.
        facebook_dir = os.path.join(user_dir, "facebook")
        if not os.path.exists(facebook_dir):
            os.makedirs(facebook_dir)

        # Save the uploaded file
        # TODO: move to background worker task
        file_name = secure_filename(upload.filename)
        print("Saving uploaded file")  # TODO: move to async user output
        try:
            upload.save(os.path.join(facebook_dir, file_name))
        except:
            # Return if the user did not provide a file to upload
            # TODO: Add flash output to facebook_upload template
            flash(
                "Please make sure that you've selected a file and that it's in ZIP format.", "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload=upload_success, breadcrumb="Facebook / Upload content"
            )

        # Unzip the uploaded file
        # TODO: move to background worker task
        print("Extracting zip file")  # TODO: move to async user output
        try:
            unzip_dir = unzip(os.path.join(facebook_dir, file_name))
            try:
                # Record the location of the user's Facebook content
                deplatformr_db = sqlite3.connect(
                    "deplatformr/" + app.config["SQLALCHEMY_DATABASE_URI"][10:])
                cursor = deplatformr_db.cursor()
                cursor.execute(
                    "INSERT INTO user_directories (user_id, platform, directory) VALUES (?,?,?)", [current_user.id, "facebook", unzip_dir, ],)
                deplatformr_db.commit()
            except Exception as e:
                print(e)
        except:
            flash("Unable to extract zip file.", "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload=upload_success, breadcrumb="Facebook / Upload content"
            )

        # Parse Facebook JSON and save to SQLite
        # TODO: move to background worker task
        try:
            # TODO: move to async user output
            print("Parsing Facebook content.")
            # TODO: move to async user output
            print("Saving posts to database.")
            total_posts, max_date, min_date, profile_updates, total_media = posts_to_db(
                unzip_dir)
            # Output upload stats
            flash("Saved " + str(total_posts[0]) + " posts between " + min_date[0] + " and " + max_date[0] + ". This includes " + str(
                profile_updates) + " profile updates. " + str(total_media[0]) + " media files were linked.", "alert-success")
            upload_success = True
        except Exception as e:
            flash("Are you sure this is a Facebook zip file? " +
                  str(e), "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload=upload_success, breadcrumb="Facebook / Upload content")

        # TODO: ENCRYPT FILES

        # TODO: Add uploaded and parsed Facebook files to Filecoin

    return render_template("facebook/facebook-upload.html", upload=upload_success, breadcrumb="Facebook / Upload content")


@ app.route('/facebook-view')
@ login_required
def facebook_view():

    day = datetime.now().strftime("%d")
    month_script = datetime.now().strftime("%b")

    return render_template("facebook/facebook-view.html", breadcrumb="Facebook / View content", this_day=day, this_month=month_script)


@ app.route('/facebook-memories')
@ login_required
def facebook_memories():

    return render_template("facebook/facebook-memories.html", breadcrumb="Facebook / View content / Memories")


@ app.route('/facebook-manage')
@ login_required
def facebook_manage():
    return render_template("facebook/facebook-manage.html", breadcrumb="Facebook / Manage content")
