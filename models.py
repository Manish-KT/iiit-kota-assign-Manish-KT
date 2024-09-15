from app import db

class Restaurant(db.Model):
    """
    Represents a restaurant in the database.

    Attributes:
        id (int): The primary key for the restaurant.
        name (str): The name of the restaurant.
        country_code (str): The country code of the restaurant.
        city (str): The city where the restaurant is located.
        address (str): The address of the restaurant.
        locality (str): The locality of the restaurant.
        locality_verbose (str): The detailed locality information.
        longitude (float): The longitude coordinate of the restaurant.
        latitude (float): The latitude coordinate of the restaurant.
        cuisines (str): The types of cuisines offered by the restaurant.
        average_cost_for_two (int): The average cost for two people.
        currency (str): The currency used.
        has_table_booking (str): Whether table booking is available.
        has_online_delivery (str): Whether online delivery is available.
        is_delivering_now (str): Whether the restaurant is currently delivering.
        switch_to_order_menu (str): Whether there's a switch to order menu.
        price_range (int): The price range of the restaurant.
        aggregate_rating (float): The aggregate rating of the restaurant.
        rating_color (str): The color associated with the rating.
        rating_text (str): The text associated with the rating.
        votes (int): The number of votes received.
    """
    __tablename__ = 'restaurant'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    country_code = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    locality = db.Column(db.String, nullable=True)
    locality_verbose = db.Column(db.String, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    cuisines = db.Column(db.String, nullable=True)
    average_cost_for_two = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String, nullable=True)
    has_table_booking = db.Column(db.String, nullable=True)
    has_online_delivery = db.Column(db.String, nullable=True)
    is_delivering_now = db.Column(db.String, nullable=True)
    switch_to_order_menu = db.Column(db.String, nullable=True)
    price_range = db.Column(db.Integer, nullable=True)
    aggregate_rating = db.Column(db.Float, nullable=True)
    rating_color = db.Column(db.String, nullable=True)
    rating_text = db.Column(db.String, nullable=True)
    votes = db.Column(db.Integer, nullable=True)

    def serialize(self):
        """
        Convert the restaurant instance to a dictionary.

        Returns:
            dict: A dictionary representation of the restaurant instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code,
            'city': self.city,
            'address': self.address,
            'locality': self.locality,
            'locality_verbose': self.locality_verbose,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'cuisines': self.cuisines,
            'average_cost_for_two': self.average_cost_for_two,
            'currency': self.currency,
            'has_table_booking': self.has_table_booking,
            'has_online_delivery': self.has_online_delivery,
            'is_delivering_now': self.is_delivering_now,
            'switch_to_order_menu': self.switch_to_order_menu,
            'price_range': self.price_range,
            'aggregate_rating': self.aggregate_rating,
            'rating_color': self.rating_color,
            'rating_text': self.rating_text,
            'votes': self.votes
        }

    def to_dict(self):
        """
        Convert the restaurant instance to a simplified dictionary.

        Returns:
            dict: A simplified dictionary representation of the restaurant instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'cuisines': self.cuisines,
            'locality_verbose': self.locality_verbose,
            'aggregate_rating': self.aggregate_rating,
            'average_cost_for_two': self.average_cost_for_two,
            'has_online_delivery': self.has_online_delivery
            # Add any other fields you want to include
        }
