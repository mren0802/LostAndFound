from app import db
from models import LostAndFoundItem

def create_tables():
    # Creates all tables
    db.create_all()

def seed_database():
    # Seeds the database with initial data
    sample_item = LostAndFoundItem(name="Sample Item", description="Sample Description", is_lost=True)
    db.session.add(sample_item)
    db.session.commit()

if __name__ == "__main__":
    create_tables()
    seed_database()
