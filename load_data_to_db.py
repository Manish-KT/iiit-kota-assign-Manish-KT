import pandas as pd
from models import Restaurant
from app import db

def load_data_to_sqlite(file_path, flask_app):
    """
    Load data from a CSV file into the SQLite database using SQLAlchemy ORM.

    Args:
        file_path (str): The path to the CSV file containing the data.
        flask_app (Flask): The Flask application instance used to access the database context.

    Raises:
        Exception: If an error occurs during the data loading process.
    """
    try:
        # Load data into a DataFrame
        df = pd.read_csv(file_path, encoding='latin1')
        print("Data loaded successfully into DataFrame")

        # Ensure the database is created and connected
        with flask_app.app_context():
            # Drop existing tables and create new ones
            db.drop_all()
            db.create_all()

            # Convert DataFrame to SQL and add to session
            for _, row in df.iterrows():
                restaurant = Restaurant(
                    id=row['Restaurant ID'],
                    name=row['Restaurant Name'],
                    country_code=row['Country Code'],
                    city=row['City'],
                    address=row['Address'],
                    locality=row['Locality'],
                    locality_verbose=row['Locality Verbose'],
                    longitude=row['Longitude'],
                    latitude=row['Latitude'],
                    cuisines=row['Cuisines'],
                    average_cost_for_two=row['Average Cost for two'],
                    currency=row['Currency'],
                    has_table_booking=row['Has Table booking'],
                    has_online_delivery=row['Has Online delivery'],
                    is_delivering_now=row['Is delivering now'],
                    switch_to_order_menu=row['Switch to order menu'],
                    price_range=row['Price range'],
                    aggregate_rating=row['Aggregate rating'],
                    rating_color=row['Rating color'],
                    rating_text=row['Rating text'],
                    votes=row['Votes']
                )
                db.session.add(restaurant)

            db.session.commit()
            print("Data loaded successfully into SQLite database")
        
    except Exception as e:
        print(f"An error occurred: {e}")
