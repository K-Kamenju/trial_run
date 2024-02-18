from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, time
from sqlalchemy import or_
from sqlalchemy import desc, asc, func
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Users, Events, Fun_times, Products, Likes, Comment_events, Comment_fun_times, Reviews, Wishlists
from datetime import timedelta

import bcrypt


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
    return jsonify({'message': 'Welcome to our App API'})


'''

START OF PROFILE ROUTES

'''


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = Users(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username = data['username'],
        email=data['email'],
        password=hashed_password,
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
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email and not username:
        return jsonify(message="Email or username is required"), 400

    user = Users.query.filter(or_(Users.email == email, Users.username == username)).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid email, username, or password"), 401

# Route to get a specific user by id
@app.route('/users/<int:user_id>', methods=['GET']) 
def get_user(user_id):
    user = Users.query.get(user_id)
    if user:
        return jsonify({'user': {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'username': user.username, 'phone_no': user.phone_no, 'category': user.category, 'image_url': user.image_url, 'gender': user.gender}})
    else:
        return jsonify(message="User not found"), 404

@app.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    new_password = data.get('new_password')
    if not new_password:
        return jsonify({'message': 'New password not provided'}), 400
    
    # Hash the new password before assigning it
    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    user.password = hashed_new_password
    db.session.commit()
    return jsonify({'message': 'Password reset successfully'})


@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    
    if user:
        # Serialize user data
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_no': user.phone_no,
            'category': user.category,
            'image_url': user.image_url,
            'gender': user.gender
        }
        return jsonify(user_data), 200
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
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone_no = data.get('phone_no', user.phone_no)
        user.category = data.get('category', user.category)
        user.image_url = data.get('image_url', user.image_url)
        user.gender = data.get('gender', user.gender)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    else:
        return jsonify(message="User not found"), 404



'''

END OF PROFILE ROUTES

'''




'''

START OF EVENT ROUTES

'''


# Routes for Events
@app.route('/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    output = [{
        'id': event.id, 
        'title': event.title, 
        'description': event.description, 
        'start_time': event.start_time, 
        'end_time': event.end_time, 
        'date_of_event': event.date_of_event,
        'comments':[{
            'id': comment.id,
            'text': comment.text, 
            'image': comment.user.image_url,
            'username': comment.user.username    
        } for comment in event.comments]

        } for event in events]
    return jsonify({'events': output})

@app.route('/user-events', methods=['GET'])
@jwt_required()
def get_user_events():
    current_user = get_jwt_identity()
    user_events = Events.query.filter_by(user_id=current_user).all()
    
    output = []
    for event in user_events:
        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_time': event.start_time.strftime('%I:%M %p'),  # Format start time
            'end_time': event.end_time.strftime('%I:%M %p'),  # Format end time
            'date_of_event': event.date_of_event.strftime('%d %b %Y'),  # Format date
            'comments': []
        }
        
        # Fetch comments for the current event
        comments = Comment_events.query.filter_by(event_id=event.id).all()
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'text': comment.text,
                'username': comment.user.username,
                'image_url': comment.user.image_url
            }
            event_data['comments'].append(comment_data)
        
        output.append(event_data)
    
    return jsonify({'user_events': output})


@app.route('/add-event', methods=['POST'])
@jwt_required()
def add_event():
    current_user = get_jwt_identity()
    data = request.get_json()

    # Parse date strings into datetime objects
    date_of_event = datetime.strptime(data['date_of_event'], '%d %b %Y')
    start_time = datetime.strptime(data['start_time'], '%I:%M %p').time()
    end_time = datetime.strptime(data['end_time'], '%I:%M %p').time()

    # Combine date and time into datetime objects
    start_datetime = datetime.combine(date_of_event, start_time)
    end_datetime = datetime.combine(date_of_event, end_time)

    new_event = Events(
        title=data['title'],
        description=data['description'],
        start_time=start_datetime,
        end_time=end_datetime,
        date_of_event=date_of_event,
        image_url=data.get('image_url'),
        user_id=current_user
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'New event created!'})

@app.route('/update-event/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    current_user = get_jwt_identity()
    event = Events.query.filter_by(id=event_id, user_id=current_user).first()
    if not event:
        return jsonify({'message': 'Event not found or you are not authorized to update this event'}), 404

    data = request.get_json()

    # Parse date string into datetime object if provided
    if 'date_of_event' in data:
        event.date_of_event = datetime.strptime(data['date_of_event'], '%d %b %Y')

    # Parse start time string into time object if provided
    if 'start_time' in data:
        start_time = datetime.strptime(data['start_time'], '%I:%M %p').time()

    # Parse end time string into time object if provided
    if 'end_time' in data:
        end_time = datetime.strptime(data['end_time'], '%I:%M %p').time()

    # Combine date_of_event with start_time and end_time to create datetime objects
    if 'date_of_event' in data and 'start_time' in data:
        event.start_time = datetime.combine(event.date_of_event, start_time)

    if 'date_of_event' in data and 'end_time' in data:
        event.end_time = datetime.combine(event.date_of_event, end_time)

    # Update other fields
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.image_url = data.get('image_url', event.image_url)

    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})


@app.route('/delete-event/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user = get_jwt_identity()
    event = Events.query.filter_by(id=event_id, user_id=current_user).first()
    if not event:
        return jsonify({'message': 'Event not found or you are not authorized to delete this event'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})


@app.route('/comment-event/<int:event_id>', methods=['POST'])
@jwt_required()
def comment_event(event_id):
    current_user = get_jwt_identity()
    event = Events.query.get(event_id)
    
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    data = request.get_json()
    comment_text = data.get('text')
    
    if not comment_text:
        return jsonify({'message': 'Comment text is required'}), 400
    
    new_comment = Comment_events(
        text=comment_text,
        user_id=current_user,
        event_id=event_id
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment added successfully'})

@app.route('/delete-comment-event/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment_events.query.get(comment_id)
    
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    
    if comment.user_id != current_user:
        return jsonify({'message': 'You are not authorized to delete this comment'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'})

'''

END OF EVENT ROUTES

'''




'''

START OF FUNTIME ROUTES

'''


# Routes for Fun_times
@app.route('/fun_times', methods=['GET'])
def get_fun_times():
    fun_times = Fun_times.query.all()
    
    output = []
    for fun_time in fun_times:
        total_likes = db.session.query(func.count(Likes.id)).filter(Likes.fun_time_id == fun_time.id).scalar()
        fun_time_data = {
            'id': fun_time.id, 
            'description': fun_time.description, 
            'image_url': fun_time.image_url, 
            'category': fun_time.category,
            'total_likes': total_likes,
            'comments': [{
                'id': comment.id,
                'text': comment.text,  
                'username': comment.user.username    
            } for comment in fun_time.comments]
        }
        output.append(fun_time_data)
    
    return jsonify({'fun_times': output})

@app.route('/add-fun_time', methods=['POST'])
@jwt_required()
def add_fun_time():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_fun_time = Fun_times(description=data['description'], image_url=data['image_url'], category=data['category'], user_id=current_user)
    db.session.add(new_fun_time)
    db.session.commit()
    return jsonify({'message': 'New Fun-Time created!'})

@app.route('/update-fun_time/<int:fun_time_id>', methods=['PUT'])
@jwt_required()
def update_fun_time(fun_time_id):
    current_user = get_jwt_identity()
    fun_time = Fun_times.query.filter_by(id=fun_time_id, user_id=current_user).first()
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
    fun_time = Fun_times.query.filter_by(id=fun_time_id, user_id=current_user).first()
    if not fun_time:
        return jsonify({'message': 'Fun-Time not found or you are not authorized to delete this Fun-Time'}), 404
    db.session.delete(fun_time)
    db.session.commit()
    return jsonify({'message': 'Fun-Time deleted successfully'})

# Route for most liked Fun-Time
@app.route('/most-liked-fun-time', methods=['GET'])
def most_liked_fun_time():
    most_liked = db.session.query(Fun_times, func.count(Likes.id).label('like_count')).\
        outerjoin(Likes).\
        group_by(Fun_times).\
        order_by(func.count(Likes.id).desc()).\
        first()

    if not most_liked:
        return jsonify({'message': 'No Fun-Time found'}), 404

    fun_time, like_count = most_liked
    return jsonify({
        'most_liked_fun_time': {
            'id': fun_time.id,
            'description': fun_time.description,
            'category': fun_time.category,
            'image_url': fun_time.image_url,
            'like_count': like_count
        }
    })



'''

END OF FUNTIME ROUTES

'''



'''

START OF MARKETPLACE ROUTES

'''


@app.route('/marketplace', methods=['GET'])
def get_marketplace():
    products = Products.query.all()
    output = []
    for product in products:
        # Calculate the average rating for the product
        average_rating = db.session.query(func.avg(Reviews.rating)).filter(Reviews.product_id == product.id).scalar()
        if average_rating is None:
            average_rating = 0  # If there are no reviews, set average rating to 0
        else:
            average_rating = round(average_rating, 1)  # Round the average rating to one decimal place
        
        # Get the reviews associated with the product
        reviews = []
        for review in product.reviews:
            review_data = {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'username': review.user.username,  # Get the username of the user who posted the review
                'user_image_url': review.user.image_url  # Get the image URL of the user who posted the review
            }
            reviews.append(review_data)
        
        # Construct the product data including the reviews
        product_data = {
            'id': product.id, 
            'title': product.title, 
            'description': product.description,
            'price': product.price, 
            'image_url': product.image_url, 
            'category': product.category,
            'average_rating': average_rating,  # Include the average rating in the response
            'reviews': reviews  # Include the reviews associated with the product
        }
        output.append(product_data)
    
    return jsonify({'products': output})

# Route to get a specific product by id
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Calculate the average rating for the product
    average_rating = db.session.query(func.avg(Reviews.rating)).filter(Reviews.product_id == product.id).scalar()
    if average_rating is None:
        average_rating = 0  # If there are no reviews, set average rating to 0
    else:
            average_rating = round(average_rating, 1)
                
    reviews = []
    for review in product.reviews:
        review_data = {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'username': review.user.username,  # Get the username of the user who posted the review
            'user_image_url': review.user.image_url  # Get the image URL of the user who posted the review
        }
        reviews.append(review_data)
    
    return jsonify({'product': {
        'id': product.id, 
        'username': product.user.last_name,
        'phone_number': product.user.phone_no,
        'title': product.title, 
        'description': product.description, 
        'price': product.price,
        'image_url': product.image_url,
        'category': product.category,
        'average_rating': average_rating,  # Include the average rating in the response
        'reviews':reviews
    }})


# Route to get products created by the logged-in user
@app.route('/my-products', methods=['GET'])
@jwt_required()
def get_my_products():
    current_user = get_jwt_identity()
    products = Products.query.filter_by(user_id=current_user).all()
    output = []
    for product in products:
        # Calculate the average rating for each product
        average_rating = db.session.query(func.avg(Reviews.rating)).filter(Reviews.product_id == product.id).scalar()
        if average_rating is None:
            average_rating = 0  # If there are no reviews, set average rating to 0
        else:
            average_rating = round(average_rating, 1)  # Round the average rating to one decimal place
            
        reviews = []
        for review in product.reviews:
            review_data = {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'username': review.user.username,  # Get the username of the user who posted the review
                'user_image_url': review.user.image_url  # Get the image URL of the user who posted the review
            }
        reviews.append(review_data)
        
        product_data = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'category': product.category,
            'average_rating': average_rating,
            'reviews': reviews
        }
        output.append(product_data)
    return jsonify({'my_products': output})


# Route to create a new product
@app.route('/create-product', methods=['POST'])
@jwt_required()
def create_product():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_product = Products(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        image_url=data['image_url'], 
        category=data['category'],
        user_id= current_user
        
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})

# Route to update a product
@app.route('/update-product/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    product = Products.query.filter_by(id=product_id).first()
    
    # Check if the product exists
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Check if the current user is the owner of the product
    if product.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

# Route to delete a product
@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user = get_jwt_identity()
    product = Products.query.filter_by(id=product_id).first()
    
    # Check if the product exists
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Check if the current user is the owner of the product
    if product.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 401
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

def get_products_by_category(category):
    products = Products.query.filter_by(category=category).all()
    output = []
    for product in products:
        # Calculate the average rating for each product
        average_rating = db.session.query(func.avg(Reviews.rating)).filter(Reviews.product_id == product.id).scalar()
        if average_rating is None:
            average_rating = 0  # If there are no reviews, set average rating to 0
        else:
            average_rating = round(average_rating, 1)  # Round the average rating to one decimal place

        # Get reviews associated with the product
        reviews = [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'username': review.user.username,
            'user_image_url': review.user.image_url
        } for review in product.reviews]

        product_data = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'category': product.category,
            'average_rating': average_rating,
            'reviews': reviews
        }
        output.append(product_data)
    return output

# Route to the tech category in the market place
@app.route('/marketplace/tech', methods=['GET'])
def get_tech_category():
    return jsonify({'products': get_products_by_category('Tech')})

# Route to the food category in the market place
@app.route('/marketplace/food', methods=['GET'])
def get_food_category():
    return jsonify({'products': get_products_by_category('Food')})

# Route to accessories category in the market place
@app.route('/marketplace/accessories', methods=['GET'])
def get_accessories_category():
    return jsonify({'products': get_products_by_category('Accessories')})

# Route to clothing category in the market place
@app.route('/marketplace/clothing', methods=['GET'])
def get_clothing_category():
    return jsonify({'products': get_products_by_category('Clothing')})

# Route to art category in the market place
@app.route('/marketplace/art', methods=['GET'])
def get_art_category():
    return jsonify({'products': get_products_by_category('Art')})


# Wishlist Routes
@app.route('/wishlists/add/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_wishlists(product_id):
    current_user_id = get_jwt_identity()
    wishlists_item = Wishlists.query.filter_by(user_id=current_user_id, product_id=product_id).first()
    if wishlists_item:
        return jsonify({'message': 'Product already in wishlists'}), 400
    new_wishlists_item = Wishlists(user_id=current_user_id, product_id=product_id)
    db.session.add(new_wishlists_item)
    db.session.commit()
    return jsonify({'message': 'Product added to wishlists successfully'}), 201

@app.route('/wishlists', methods=['GET'])
@jwt_required()
def get_wishlists():
    current_user_id = get_jwt_identity()
    wishlists_items = Wishlists.query.filter_by(user_id=current_user_id).all()
    wishlists = []
    for item in wishlists_items:
        product = Products.query.get(item.product_id)
        user = Users.query.get(product.user_id)
        wishlists.append({
            'product_id': product.id,
            'product_title': product.title,
            'product_description': product.description,
            'product_price': product.price,
            'product_image_url': product.image_url,
            'product_category': product.category,
            'seller_first_name': user.first_name,
            'seller_last_name': user.last_name,
            'seller_email': user.email,
            'seller_phone_number': user.phone_no,
            'seller_image_url': user.image_url
        })
    return jsonify({'wishlists': wishlists})


@app.route('/wishlists/remove/<int:wishlists_item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlists(wishlists_item_id):
    current_user_id = get_jwt_identity()
    wishlists_item = Wishlists.query.filter_by(id=wishlists_item_id, user_id=current_user_id).first()
    if not wishlists_item:
        return jsonify({'message': 'Wishlists item not found'}), 404
    db.session.delete(wishlists_item)
    db.session.commit()
    return jsonify({'message': 'Product removed from wishlists successfully'})



'''

END OF MARKETPLACE ROUTES

'''




'''

START OF STUDENT ROUTES

'''






'''

END OF STUDENT ROUTES

'''

if __name__ == '__main__':
    app.run(debug=True)
