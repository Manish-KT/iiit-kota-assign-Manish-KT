from app import create_app
from load_data_to_db import load_data_to_sqlite
from flask_cors import CORS
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def run_flask_app():
    """
    Create and run the Flask application.
    """
    flask_app = create_app()
    flask_app.run(debug=True)

def load_data():
    """
    Load data into the SQLite database using the provided CSV file.
    """
    flask_app = create_app()
    with flask_app.app_context():
        print("Loading data into SQLite database...")
        load_data_to_sqlite('data/zomato.csv', flask_app)

if __name__ == "__main__":
    # Start Flask app
    print("Starting Flask app...")
    run_flask_app()
    print("Flask app started...")

    # Load data into SQLite database
    load_data()
