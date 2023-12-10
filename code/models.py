from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LostAndFoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_lost = db.Column(db.Boolean)
    # adding an image path
    image_path = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description, is_lost):
        self.name = name
        self.description = description
        self.is_lost = is_lost
