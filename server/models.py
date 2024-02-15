from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Relationships
    posted_events = db.relationship('Events', backref='author', lazy=True)
    posted_fun_times = db.relationship('Fun_times', backref='author', lazy=True)
    comments_on_events = db.relationship('Comment_events', backref='commenter', lazy=True)
    comments_on_fun_times = db.relationship('Comment_fun_times', backref='commenter', lazy=True)

    products = db.relationship('Products', backref='user', lazy=True)
    reviews = db.relationship('Reviews', backref='user', lazy=True)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    date_of_event = db.Column(db.Date)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    comments = db.relationship('Comment_events', backref='event', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    price = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    category = db.Column(db.String(50))
    wishlist = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Reviews', backref='product', lazy=True)

class Fun_times(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    comments = db.relationship('Comment_fun_times', backref='fun_time', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('Likes', backref='fun_time', lazy=True)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_time_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Comment_events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Comment_fun_times(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_times_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))