import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from flask_user import login_required, current_user
from deplatformr import app, db
from deplatformr.helpers.helpers import unzip
from deplatformr.helpers.facebook_helpers import posts_to_db, activate_hyperlinks, cut_hyperlinks, clean_nametags


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
        user_dir = os.path.join(
            upload_path, str(current_user.id) + "-" + current_user.username)
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
                profile_updates) + " profile updates. " + str(total_media[0]) + " media files were uploaded.", "alert-success")
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

    deplatformr_db = sqlite3.connect(
        "deplatformr/" + app.config["SQLALCHEMY_DATABASE_URI"][10:])
    cursor = deplatformr_db.cursor()
    cursor.execute(
        "SELECT directory FROM user_directories WHERE user_id = ? AND platform = ?", (current_user.id, "facebook",),)
    directory = cursor.fetchone()

    if directory is None:
        flash("Facebook data not found.", "alert-danger")
        return render_template(
            "facebook/facebook-memories.html", breadcrumb="Facebook / View content / Memories")

    fb_dir = directory[0]
    db_name = os.path.basename(os.path.normpath(fb_dir))
    fb_db = fb_dir + "/" + str(db_name) + ".db"

    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%m")
    month_script = datetime.now().strftime("%b")
    year = datetime.now().strftime("%Y")

    facebook_db = sqlite3.connect(fb_db)
    cursor = facebook_db.cursor()
    cursor.execute("SELECT * FROM posts")
    """
    cursor.execute(
        "SELECT * FROM posts WHERE strftime('%m', timestamp) = ? AND strftime('%d', timestamp) = ? ORDER BY timestamp ASC", (month, day),)
    """
    posts = cursor.fetchall()

    media_posts = {}
    non_media_posts = {}

    for post in posts:
        if (post[3] is not None) and (post[3] > 0):

            post_year = post[1][:4]
            time_lapse = int(year) - int(post_year)
            if post[2] is not None:
                clean_post_names = clean_nametags(post[2])
                # TODO: figure out how to activate post hyperlinks within the post text
                # parsed_post, url_count = activate_hyperlinks(clean_post_names)
                parsed_post, urls = cut_hyperlinks(clean_post_names)

            cursor.execute(
                "SELECT * FROM media WHERE post_id = ?", (post[0],),)
            media = cursor.fetchall()

            files = {}
            for file in media:
                if (file[3] is not None):
                    if file[3] != post[2]:
                        clean_post_names = clean_nametags(file[3])
                        file_parsed_post, file_urls = cut_hyperlinks(
                            clean_post_names)
                    else:
                        file_parsed_post = None
                        file_urls = None
                else:
                    if (post[2] is None) or (post[2] == ""):
                        file_parsed_post = file[2]
                        file_urls = None
                extension = os.path.splitext(file[6])
                if extension[1] == ".mp4":
                    mimetype = "video"
                else:
                    mimetype = "image"
                filepath = file[6]
                files.update({file[0]: {
                    "file_post": file_parsed_post,
                    "urls": file_urls,
                    "mimetype": mimetype}})
                # reset parsed_post so that it's not re-used for entries that don't have a file[3]
                file_parsed_post = None
                file_urls = None

            media_posts.update({post[0]: {"post_year": post_year, "time_lapse": time_lapse,
                                          "post": parsed_post, "urls": urls, "files": files}})

            # reset parsed_post so that it's not re-used for entries that don't have a post[2]
            parsed_post = None

    if len(posts) > len(media_posts):
        for post in posts:
            if (post[3] is None) or (post[3] == 0):

                # some entries can be completely blank except for a timestamp
                if post[2] is None and post[4] is None and post[5] is None:
                    continue

                post_year = post[1][:4]
                time_lapse = int(year) - int(post_year)
                if post[2] is not None:
                    clean_post_names = clean_nametags(post[2])
                    # TODO: figure out how to activate post hyperlinks within the post text
                    # parsed_post, url_count = activate_hyperlinks(clean_post_names)
                    parsed_post, urls = cut_hyperlinks(clean_post_names)

                if post[4] is not None and len(urls) == 0:
                    urls = []
                    urls.append(post[4])

                non_media_posts.update({post[0]: {"post_year": post_year,
                                                  "time_lapse": time_lapse,
                                                  "post": parsed_post,
                                                  "url_label": post[5],
                                                  "urls": urls}})

                # reset parsed_post so that it's not re-used for entries that don't have a post[2]
                parsed_post = None

    return render_template("facebook/facebook-memories.html", breadcrumb="Facebook / View content / Memories", month_script=month_script, day=day, media_posts=media_posts, non_media_posts=non_media_posts)


@ app.route('/facebook-manage')
@ login_required
def facebook_manage():
    return render_template("facebook/facebook-manage.html", breadcrumb="Facebook / Manage content")
