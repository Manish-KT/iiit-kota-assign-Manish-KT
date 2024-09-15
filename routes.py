from flask import render_template, request, abort, redirect, url_for, jsonify
from models import Restaurant
import math
import os
from werkzeug.utils import secure_filename
import requests
from io import BytesIO
from PIL import Image
from classification.ml_model import FoodClassifier

# Create an instance of the FoodClassifier class
classifier = FoodClassifier('classification/food41_model.h5', 'classification/food_to_broad_category_mapping.json')

INDEX_HTML = 'index.html'
IMAGE_SEARCH_HTML = 'image_search.html'
RESTAURANT_DETAILS_HTML = 'restaurant_details.html'
RESTAURANT_LIST_HTML = 'restaurant_list.html'

def allowed_file(filename):
    """
    Check if the file has an allowed extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_image_from_url(image_url, upload_folder):
    """
    Download an image from a URL and save it to the specified folder.

    Args:
        image_url (str): The URL of the image.
        upload_folder (str): The folder where the image will be saved.

    Returns:
        str: The path where the image was saved.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    filename = secure_filename(image_url.split("/")[-1])
    file_path = os.path.join(upload_folder, filename)
    img.save(file_path)
    return file_path

def find_restaurants_by_broad_categories(broad_categories):
    """
    Find restaurants that match any of the specified broad categories.

    Args:
        broad_categories (list): A list of broad categories to search for.

    Returns:
        list: A list of Restaurant objects that match the categories.
    """
    return Restaurant.query.filter(Restaurant.cuisines.in_(broad_categories)).all()

def register_routes(app, db):
    """
    Register application routes with the Flask app.

    Args:
        app (Flask): The Flask application instance.
        db (SQLAlchemy): The SQLAlchemy database instance.
    """
    @app.route('/all_restaurants')
    def show_all_restaurants():
        """
        Display all restaurants with pagination.

        Returns:
            str: Rendered HTML template with a list of restaurants.
        """
        page = request.args.get('page', 1, type=int)
        per_page = 10
        restaurants = Restaurant.query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template(RESTAURANT_LIST_HTML, restaurants=restaurants, pagination=restaurants)
    
    @app.route('/')
    def home():
        """
        Display the home page.

        Returns:
            str: Rendered HTML template for the home page.
        """
        print("----------------" + os.getcwd())
        return render_template(INDEX_HTML)
    
    @app.route('/search_restaurant', methods=['GET'])
    def search_restaurant():
        """
        Search for restaurants based on various criteria.

        Returns:
            str: Rendered HTML template with search results.
        """
        restaurant_id = request.args.get('restaurant_id')
        cuisine = request.args.get('cuisine')
        country = request.args.get('country')
        cost_for_two = request.args.get('cost_for_two')
        rating = request.args.get('rating')
        delivery = request.args.get('delivery')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius_km = request.args.get('radius')

        query = Restaurant.query

        if restaurant_id and restaurant_id != 'any':
            query = query.filter_by(id=restaurant_id)

        if cuisine and cuisine != 'any':
            query = query.filter(Restaurant.cuisines.ilike(f'%{cuisine}%'))

        if country and country != 'any':
            query = query.filter_by(country=country)

        if cost_for_two and cost_for_two != 'any':
            if cost_for_two == 'under-500':
                query = query.filter(Restaurant.average_cost_for_two < 500)
            elif cost_for_two == '500-1000':
                query = query.filter(Restaurant.average_cost_for_two.between(500, 1000))
            elif cost_for_two == '1000-2000':
                query = query.filter(Restaurant.average_cost_for_two.between(1000, 2000))
            elif cost_for_two == 'above-2000':
                query = query.filter(Restaurant.average_cost_for_two > 2000)

        if rating and rating != 'any':
            query = query.filter(Restaurant.aggregate_rating >= int(rating))

        if delivery and delivery != 'any':
            query = query.filter(Restaurant.has_online_delivery == (delivery == 'online'))

        if latitude and longitude and radius_km:
            def distance(origin, destination):
                lat1, lon1 = origin
                lat2, lon2 = destination
                radius = 6371  # km
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                return radius * c

            def filter_by_location(restaurant):
                restaurant_coords = (restaurant.latitude, restaurant.longitude)
                user_coords = (float(latitude), float(longitude))
                return distance(user_coords, restaurant_coords) <= float(radius_km)

            all_restaurants = query.all()
            restaurants_within_range = [r for r in all_restaurants if filter_by_location(r)]
            return render_template(INDEX_HTML, restaurants=restaurants_within_range)

        restaurants = query.all()
        return render_template(INDEX_HTML, restaurants=restaurants)

    @app.route('/restaurant/<int:restaurant_id>')
    def restaurant_details(restaurant_id):
        """
        Display details of a specific restaurant.

        Args:
            restaurant_id (int): The ID of the restaurant.

        Returns:
            str: Rendered HTML template with restaurant details.
        """
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return render_template(RESTAURANT_DETAILS_HTML, restaurant=restaurant)
    
    @app.route('/image_search', methods=['POST'])
    def image_search():
        """
        Handle image classification via URL or file upload and find restaurants based on the classification.

        Returns:
            str: Rendered HTML template with search results or error message.
        """
        file_path = None

        if 'upload_image' in request.files and request.files['upload_image'].filename:
            file = request.files['upload_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

        if 'image_url' in request.form and request.form['image_url']:
            image_url = request.form['image_url']
            try:
                file_path = save_image_from_url(image_url, app.config['UPLOAD_FOLDER'])
            except Exception as e:
                return jsonify({'error': str(e)}), 400

        if file_path:
            _, broad_categories = classifier.predict_and_map_class(file_path)
            if broad_categories:
                return render_template(INDEX_HTML, restaurants=find_restaurants_by_broad_categories(broad_categories))

        return 'No valid image source provided', 400
