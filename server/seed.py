from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from faker import Faker

from models import db, Users, Events, Products, Fun_times, Likes, Comment_events, Comment_fun_times, Reviews
from app import app

fake = Faker()

def seed_data():
    # Create users
    for _ in range(50):
        user = Users(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_no=fake.phone_number(),
            password=fake.password(),
            category=random.choice(['Software Dev', 'Data Science', 'Cybersec', 'UI/UX']),
            image_url='https://example.com/john.jpg',
            gender=random.choice(['male', 'female']),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            username=fake.user_name()
        )
        db.session.add(user)
    db.session.commit()

    # Create categories
    product_categories = ['Food', 'Tech', 'Accessories', 'Clothing', 'Art']
    fun_time_categories = ['Funny', 'Educational', 'Events']

    # Create products
    for _ in range(50):
        product = Products(
            title=fake.word(),
            description=fake.sentence(),
            image_url=fake.image_url(),
            price=random.randint(10, 1000),
            category=random.choice(product_categories),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=random.randint(1, 50)
        )
        db.session.add(product)
    db.session.commit()

    # Create reviews for products
    for product in Products.query.all():
        for _ in range(random.randint(1, 5)):
            review = Reviews(
                text=fake.paragraph(),
                user_id=random.randint(1, 50),
                rating=random.randint(1, 5),
                product_id=product.id
            )
            db.session.add(review)
    db.session.commit()

    # Create events
    for _ in range(20):
        event = Events(
            title=fake.sentence(),
            description=fake.paragraph(),
            image_url=fake.image_url(),
            start_time=fake.date_time_this_month(),
            end_time=fake.date_time_this_month(),
            date_of_event=fake.date_this_month(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=random.randint(1, 50)
        )
        db.session.add(event)
    db.session.commit()

    # Create fun times
    for _ in range(30):
        fun_time = Fun_times(
            description=fake.paragraph(),
            image_url=fake.image_url(),
            category=random.choice(fun_time_categories),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=random.randint(1, 50)
        )
        db.session.add(fun_time)
    db.session.commit()

    # Create likes for fun times
    for _ in range(50):
        like = Likes(
            user_id=random.randint(1, 50),
            fun_time_id=random.randint(1, 30)
        )
        db.session.add(like)
    db.session.commit()

    # Create comments for events
    for event in Events.query.all():
        for _ in range(random.randint(1, 5)):
            comment_event = Comment_events(
                text=fake.paragraph(),
                user_id=random.randint(1, 50),
                event_id=event.id
            )
            db.session.add(comment_event)
    db.session.commit()

    # Create comments for fun times
    for fun_time in Fun_times.query.all():
        for _ in range(random.randint(1, 5)):
            comment_fun_time = Comment_fun_times(
                text=fake.paragraph(),
                user_id=random.randint(1, 50),
                fun_time_id=fun_time.id  # Corrected attribute name
            )
            db.session.add(comment_fun_time)
    db.session.commit()

    
if __name__ == '__main__':
   with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()
        print("Data seeded successfully!")

# {
#   "description":"Come to swim with us",
#   "category":""
# }

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODA4MjQ4OCwianRpIjoiZjJlMTQyOTItYzgyMS00OTg4LWFiODQtMTM4ZTI4MzBkMjRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NTEsIm5iZiI6MTcwODA4MjQ4OCwiY3NyZiI6IjBjZTM5YTc5LWExYTEtNDVlMi05ODlkLTJmNmRiMzQ5Y2M0MCIsImV4cCI6MTcwODE2ODg4OH0.odP6CZi4woGa9aGMfzmShLuV3B4dkolU_im9PrYTLOU