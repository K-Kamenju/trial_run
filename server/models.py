from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, UniqueConstraint, ForeignKey, Table


# Define metadata with a naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata =  metadata)

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Users(db.Model, SerializerMixin):
    
    serialize_rules = ('-events.user','-fun_times.user','-comments_on_events.user', '-comments_on_fun_times.user','-products.user','-reviews.user',)
    
    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    gender = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    student_id = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(55))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Relationships
    events = db.relationship('Events', backref='user', lazy=True)
    fun_times = db.relationship('Fun_times', backref='user', lazy=True)
    comments_on_events = db.relationship('Comment_events', backref='user', lazy=True)
    comments_on_fun_times = db.relationship('Comment_fun_times', backref='user', lazy=True)
    products = db.relationship('Products', backref='user', lazy=True)
    reviews = db.relationship('Reviews', backref='user', lazy=True)

class Events(db.Model, SerializerMixin):
    
    serialize_rules = ('-users.events','-comments.event',)
    
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    date_of_event= db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))
    date_of_event = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment_events', backref='event', lazy=True)
    

class Products(db.Model, SerializerMixin):
    
    serialize_rules = ('-users.products', '-reviews.product',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))
    wishlist = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Reviews', backref='product', lazy=True)

class Fun_times(db.Model, SerializerMixin):
    
    serialize_rules = ('-users.fun_times','-comments.fun_time', '-likes.fun_time',)
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    comments = db.relationship('Comment_fun_times', backref='fun_time', lazy=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    comments = db.relationship('Comment_fun_times', backref='fun_time', lazy=True) 
    likes = db.relationship('Likes', backref='fun_time', lazy=True)

class Likes(db.Model, SerializerMixin):
    
    serialize_rules =('-funtimes.likes')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_time_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Comment_events(db.Model, SerializerMixin):
    
    serialize_rules=('-users.comment_events','-events.comment_events',)
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Comment_fun_times(db.Model, SerializerMixin):
    
    serialize_rules=('-users.comment_fun_times','-fun_times.comment_fun_times',)
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fun_times_id = db.Column(db.Integer, db.ForeignKey('fun_times.id'))

class Reviews(db.Model, SerializerMixin):
    
    serialize_rules=('-users.reviews','-products.reviews',)
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    rating = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


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