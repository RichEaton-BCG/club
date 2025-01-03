from app import create_app, db

# Initialize the Flask application using the factory function
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
