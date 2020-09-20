import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from flask_user import login_required, current_user
from deplatformr import app
from deplatformr.helpers.helpers import unzip
from deplatformr.helpers.facebook_helpers import posts_to_db


@app.route('/facebook-deplatform')
@login_required
def facebook_deplatform():
    return render_template("facebook/facebook-deplatform.html", breadcrumb="Facebook / Deplatform")


@app.route('/facebook-upload', methods=["GET", "POST"])
@login_required
def facebook_upload():

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
            upload_stats = ""  # query to retrieve all current and historical upload stats
            # TODO: Add flash output to facebook_upload template
            flash("Please choose a .zip file to upload to Deplatformr", "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload_stats=upload_stats
            )

        # Unzip the uploaded file
        # TODO: move to background worker task
        print("Extracting zip file")  # TODO: move to async user output
        try:
            unzip_dir = unzip(os.path.join(facebook_dir, file_name))
        except:
            upload_stats = ""  # query to retrieve all current and historical upload stats
            flash("Unable to extract zip file.", "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload_stats=upload_stats
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
            print(str(total_posts[0]) + " posts between " +
                  min_date[0] + " and " + max_date[0] + " were saved.")
            print("Including " + str(profile_updates) + " profile updates.")
            # TODO: move to async user output
            print(str(total_media[0]) + " media files were linked.")
        except Exception as e:
            upload_stats = ""  # query to retrieve all current and historical upload stats
            flash(e, "alert-danger")
            return render_template(
                "facebook/facebook-upload.html", upload_stats=upload_stats)

        # TODO: ENCRYPT FILES

        # TODO: Add uploaded and parsed Facebook files to Filecoin

    upload_stats = ""  # query to retrieve all current and historical upload stats

    return render_template("facebook/facebook-upload.html", upload_stats=upload_stats, breadcrumb="Facebook / Upload content")


@ app.route('/facebook-view')
@ login_required
def facebook_view():
    return render_template("facebook/facebook-view.html", breadcrumb="Facebook / View content")


@ app.route('/facebook-manage')
@ login_required
def facebook_manage():
    return render_template("facebook/facebook-manage.html", breadcrumb="Facebook / Manage content")
