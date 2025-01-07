''' Stand alone code for initializing the database.
This script should be run outside of the Flask application context.'''

import sys
import os
print(sys.path)
from app import create_app, db

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))


# Create and configure the Flask app
app = create_app()

# Initialize the database
with app.app_context():
    db.drop_all()
    #db.create_all()
    print("Database tables dropped !")
