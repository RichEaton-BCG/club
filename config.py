import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///racquetball_club.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
    #STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
