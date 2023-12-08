# Defines basic structure of Flask app and calls the main routes

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, LostAndFoundItem
from forms import LostItemForm, FoundItemForm

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:password@localhost:3306/lostandfound"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "food"


# bind SQLAlchemy to Flask
db.init_app(app)

# initialize database within app context
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    try:
        items = LostAndFoundItem.query.all()
    except Exception as e:
        print(e)  # log error
        items = []
    return render_template("index.html", items=items)


@app.route("/search")
def search():
    query = request.args.get("search")
    # Perform search using the query
    search_results = LostAndFoundItem.query.filter(
        LostAndFoundItem.name.like("%" + query + "%")
    ).all()
    return render_template("search_results.html", items=search_results)


@app.route("/report_lost", methods=["GET", "POST"])
def report_lost():
    form = LostItemForm()
    if form.validate_on_submit():
        lost_item = LostAndFoundItem(
            name=form.name.data, description=form.description.data, is_lost=True
        )
        print(lost_item)
        try:
            db.session.add(lost_item)
            db.session.commit()

            flash("Item reported successfully!")

            # redirect back to homepage after submission
            return redirect(url_for("index"))

        except Exception as e:
            print(e)  # Log the error
        return redirect(url_for("index"))
    return render_template("report_lost.html", form=form)


@app.route("/report_found", methods=["GET", "POST"])
def report_found():
    form = FoundItemForm()
    if form.validate_on_submit():
        found_item = LostAndFoundItem(
            name=form.name.data, description=form.description.data, is_lost=False
        )
        try:
            db.session.add(found_item)
            db.session.commit()
        except Exception as e:
            print(e)  # Log the error
        return redirect(url_for("index"))
    return render_template("report_found.html", form=form)


"""
@app.route('/test_flash')
def test_flash():
    flash('This is a flash message test.')
    return redirect(url_for('index'))
"""

if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000
