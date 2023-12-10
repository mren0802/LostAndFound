# Defines basic structure of Flask app and calls the main routes

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, LostAndFoundItem
from forms import LostItemForm, FoundItemForm
import os
from werkzeug.utils import secure_filename

# Path for image uploads
Upload_Folder = "path/to/uploaded/images"
Allowed_Extensions = {"png", "jpg", "jpeg", "gif"}


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:password@localhost:3306/lostandfound"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "food"
app.config['Upload_Folder'] = Upload_Folder


# bind SQLAlchemy to Flask
db.init_app(app)

# initialize database within app context
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Allowed_Extensions

@app.route("/", methods=["GET"])
def index():
    try:
        items = (
            db.session.query(LostAndFoundItem)
            .filter(LostAndFoundItem.is_lost == True)
            .all()
        )
    except Exception as e:
        print(e)  # log error
        items = []
    return render_template("index.html", items=items)


@app.route("/search")
def search():
    query = request.args.get("search")
    if query:
        # filter by name and when is_lost is true
        # only show items that are lost
        search_results = LostAndFoundItem.query.filter(
            LostAndFoundItem.name.like(f"%{query}%"), LostAndFoundItem.is_lost.is_(True)
        ).all()
    else:
        search_results = []
    return render_template("search_results.html", items=search_results)


@app.route("/report_lost", methods=["GET", "POST"])
def report_lost():
    if request.method == "POST":
        lostitem_form = LostItemForm(formdata=request.form)
        if lostitem_form.validate():
            lost_item = LostAndFoundItem(
                name=lostitem_form.name.data,
                description=lostitem_form.description.data,
                is_lost=True,
            )
            try:
                db.session.add(lost_item)
                db.session.commit()

                flash("Item reported successfully!")

                # redirect back to homepage after submission
                return redirect(url_for("index"))

            except Exception as e:
                print(e)  # Log the error
            return redirect(url_for("index"))
        # else:
        #     print('Did not pass validation.')
    return render_template("report_lost.html", form=LostItemForm())


@app.route("/report_found", methods=["GET", "POST"])
def report_found():
    if request.method == "POST":
        founditem_form = FoundItemForm(formdata=request.form)
        if founditem_form.validate():
            found_item = LostAndFoundItem(
                name=founditem_form.name.data,
                description=founditem_form.description.data,
                is_lost=False,
            )
            try:
                # db.session.add(found_item)
                result = (
                    db.session.query(LostAndFoundItem)
                    .filter(
                        LostAndFoundItem.name == found_item.name,
                        LostAndFoundItem.name == found_item.name,
                    )
                    .all()
                )
                # print(result)
                for item in result:
                    item.is_lost = False
                db.session.commit()
            except Exception as e:
                print(e)  # Log the error
            return redirect(url_for("index"))
    return render_template("report_found.html", form=FoundItemForm())


"""
@app.route('/test_flash')
def test_flash():
    flash('This is a flash message test.')
    return redirect(url_for('index'))
"""

if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000
