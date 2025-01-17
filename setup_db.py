import sys
import os
from app import create_app, db
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Add the project root directory to Python path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Create and configure the Flask app
app = create_app()

# Initialize the database
with app.app_context():
    db.create_all()
    print("Database tables added!")
