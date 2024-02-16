from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Users, Events, Fun_times
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vsgewvwesvsgevafdsag'  
app.config['JWT_SECRET_KEY'] = 'vsgewvwesvsgevafdsag'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Set token expiration time
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum content length for incoming requests to 16 MB

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Market API'})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = Users(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        phone_no=data['phone_no'],
        category=data['category'],
        image_url=data.get('image_url'),
        gender=data.get('gender')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid email or password"), 401

# Route to get a specific user by id
@app.route('/users/<int:user_id>', methods=['GET']) 
def get_user(user_id):
    user = Users.query.get(user_id)
    if user:
        return jsonify({'user': {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}})
    else:
        return jsonify(message="User not found"), 404

@app.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    new_password = data.get('new_password')
    if not new_password:
        return jsonify({'message': 'New password not provided'}), 400
    
    user.password = new_password
    db.session.commit()
    return jsonify({'message': 'Password reset successfully'})

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()
    if user:
        return jsonify({'user': {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}})
    else:
        return jsonify(message="User not found"), 404

@app.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()
    if user:
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_no = data.get('phone_no', user.phone_no)
        user.category = data.get('category', user.category)
        user.image_url = data.get('image_url', user.image_url)
        user.gender = data.get('gender', user.gender)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    else:
        return jsonify(message="User not found"), 404

# Routes for Events
@app.route('/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    output = [{'id': event.id, 'title': event.title, 'description': event.description, 'start_time': event.start_time, 'end_time': event.end_time, 'date_of_event': event.date_of_event} for event in events]
    return jsonify({'events': output})

@app.route('/add-event', methods=['POST'])
@jwt_required()
def add_event():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_event = Events(title=data['title'], description=data['description'], start_time=data['start_time'], end_time=data['end_time'], date_of_event=data['date_of_event'], user_id=current_user)
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'New event created!'})

@app.route('/update-event/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    current_user = get_jwt_identity()
    event = Events.query.filter_by(id=event_id, author_id=current_user).first()
    if not event:
        return jsonify({'message': 'Event not found or you are not authorized to update this event'}), 404
    data = request.get_json()
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.start_time = data.get('start_time', event.start_time)
    event.end_time = data.get('end_time', event.end_time)
    event.date_of_event = data.get('date_of_event', event.date_of_event)
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/delete-event/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user = get_jwt_identity()
    event = Events.query.filter_by(id=event_id, author_id=current_user).first()
    if not event:
        return jsonify({'message': 'Event not found or you are not authorized to delete this event'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})

# Routes for Fun_times
@app.route('/fun_times', methods=['GET'])
def get_fun_times():
    fun_times = Fun_times.query.all()
    output = [{'id': fun_time.id, 'description': fun_time.description, 'category': fun_time.category} for fun_time in fun_times]
    return jsonify({'fun_times': output})

@app.route('/add-fun_time', methods=['POST'])
@jwt_required()
def add_fun_time():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_fun_time = Fun_times(description=data['description'], category=data['category'], author_id=current_user)
    db.session.add(new_fun_time)
    db.session.commit()
    return jsonify({'message': 'New Fun-Time created!'})

@app.route('/update-fun_time/<int:fun_time_id>', methods=['PUT'])
@jwt_required()
def update_fun_time(fun_time_id):
    current_user = get_jwt_identity()
    fun_time = Fun_times.query.filter_by(id=fun_time_id, author_id=current_user).first()
    if not fun_time:
        return jsonify({'message': 'Fun-Time not found or you are not authorized to update this Fun-Time'}), 404
    data = request.get_json()
    fun_time.description = data.get('description', fun_time.description)
    fun_time.category = data.get('category', fun_time.category)
    db.session.commit()
    return jsonify({'message': 'Fun-Time updated successfully'})

@app.route('/delete-fun_time/<int:fun_time_id>', methods=['DELETE'])
@jwt_required()
def delete_fun_time(fun_time_id):
    current_user = get_jwt_identity()
    fun_time = Fun_times.query.filter_by(id=fun_time_id, author_id=current_user).first()
    if not fun_time:
        return jsonify({'message': 'Fun-Time not found or you are not authorized to delete this Fun-Time'}), 404
    db.session.delete(fun_time)
    db.session.commit()
    return jsonify({'message': 'Fun-Time deleted successfully'})

# Route for most liked Fun-Time
@app.route('/most-liked-fun-time', methods=['GET'])
def most_liked_fun_time():
    most_liked = Fun_times.query.order_by(Fun_times.likes.desc()).first()
    if not most_liked:
        return jsonify({'message': 'No Fun-Time found'}), 404
    return jsonify({'most_liked_fun_time': {'id': most_liked.id, 'description': most_liked.description, 'category': most_liked.category}})

# Route to get all products for the market place
@app.route('/marketplace', methods=['GET'])
def get_marketplace():
    products = Products.query.all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in products]
    return jsonify({'products': output})

# Route to get a specific product by id
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({'product': {'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url}})

# Route to create a new product
@app.route('/create-product', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        image_url=data['image_url']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})

# Route to update a product
@app.route('/update-product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

# Route to delete a product
@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# Route to the tech category in the market place
@app.route('/marketplace/tech', methods=['GET'])
def get_tech_category():
    tech_products = Products.query.filter_by(category='Tech').all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in tech_products]
    return jsonify({'products': output})

# Route to the food category in the market place
@app.route('/marketplace/food', methods=['GET'])
def get_food_category():
    food_products = Products.query.filter_by(category='Food').all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in food_products]
    return jsonify({'products': output})

# Route to accesories category in the market place
@app.route('/marketplace/accessories', methods=['GET'])
def get_accessories_category():
    accessories_products = Products.query.filter_by(category='Accessories').all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in accessories_products]
    return jsonify({'products': output})

# Route to clothing category in the market place
@app.route('/marketplace/clothing', methods=['GET'])
def get_clothing_category():
    clothing_products = Products.query.filter_by(category='Clothing').all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in clothing_products]
    return jsonify({'products': output})

# Route to art category in the market place
@app.route('/marketplace/art', methods=['GET'])
def get_art_category():
    art_products = Products.query.filter_by(category='Art').all()
    output = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in art_products]
    return jsonify({'products': output})


if __name__ == '__main__':
    app.run(debug=True)
