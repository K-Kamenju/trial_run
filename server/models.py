from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# Define metadata with a naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy()

class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    gender = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    events = db.relationship('Events', backref='user', lazy=True)
    fun_times = db.relationship('Fun_times', backref='user', lazy=True)
    comments_on_events = db.relationship('Comment_events', backref='user', lazy=True)
    comments_on_fun_times = db.relationship('Comment_fun_times', backref='user', lazy=True)
    products = db.relationship('Products', backref='user', lazy=True)
    reviews = db.relationship('Reviews', backref='user', lazy=True)

class Events(db.Model, SerializerMixin):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    date_of_event = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment_events', backref='event', lazy=True)

class Products(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Reviews', backref='product', lazy=True)

class Wishlists(db.Model, SerializerMixin):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Users', backref='wishlists_items', lazy=True)
    product = db.relationship('Products', backref='wishlists_items', lazy=True)


class Fun_times(db.Model, SerializerMixin):
    __tablename__ = 'fun_times'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment_fun_times', backref='fun_time', lazy=True)
    likes = db.relationship('Likes', backref='fun_time', lazy=True)

class Likes(db.Model, SerializerMixin):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_time_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Comment_events(db.Model, SerializerMixin):
    __tablename__ = 'comment_events'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Comment_fun_times(db.Model, SerializerMixin):
    __tablename__ = 'comment_fun_times'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_time_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Reviews(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

# Serialization rules
Users.serialize_rules = (
    '-events.user',
    '-fun_times.user',
    '-comments_on_events.user',
    '-comments_on_fun_times.user',
    '-products.user',
    '-reviews.user',
)

Events.serialize_rules = (
    '-users.events',
    '-comments.event',
)

Products.serialize_rules = (
    '-users.products',
    '-reviews.product',
)

Fun_times.serialize_rules = (
    '-users.fun_times',
    '-comments.fun_time',
    '-likes.fun_time',
)

Likes.serialize_rules = (
    '-fun_times.likes',
)

Comment_events.serialize_rules = (
    '-users.comment_events',
    '-events.comment_events',
)

Comment_fun_times.serialize_rules = (
    '-users.comment_fun_times',
    '-fun_times.comment_fun_times',
)

Reviews.serialize_rules = (
    '-users.reviews',
    '-products.reviews',
)

Wishlists.serialize_rules = (
    'user.id',
    'user.first_name',
    'user.last_name', 
    'user.email',
    'user.phone_no',
    'user.image_url',
    'product.id',
    'product.title',      
    'product.description',
    'product.price'
)

# {
#   "first_name":"Mike",
#   "last_name":"Tom",
#   "email":"mike@gmail.com",
#   "password":"IAm",
#   "phone_no":"0757720955",
#   "category":"Software Dev",
#   "image_url":"Fake_url",
#   "gender":"male"
# }

# {
#       "date_of_event": "Thu, 08 Feb 2024 00:00:00 GMT",
#       "description": "Chem",
#       "end_time": "Fri, 16 Feb 2024 14:53:27 GMT",
#       "start_time": "Wed, 07 Feb 2024 09:50:53 GMT",
#       "title": "Exams."
# }