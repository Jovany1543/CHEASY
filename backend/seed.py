#!/usr/bin/env python
"""
Seed script to populate the database with dummy data for development.
Run with: pipenv run seed
"""

from app import app, db
from models import User, Item

def seed_database():
    """Populate the database with dummy users and items."""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create dummy users
        print("Creating dummy users...")
        users_data = [
            {'username': 'alice', 'password': 'password123'},
            {'username': 'bob', 'password': 'securepass456'},
            {'username': 'charlie', 'password': 'mypassword789'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(username=user_data['username'])
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        # Create dummy items
        print("Creating dummy items...")
        items_data = [
            'Buy groceries',
            'Complete project documentation',
            'Review pull requests',
            'Schedule team meeting',
            'Update database schema',
            'Write unit tests',
            'Deploy to production',
            'Fix critical bug',
        ]
        
        items = []
        for text in items_data:
            item = Item(text=text)
            items.append(item)
            db.session.add(item)
        
        db.session.commit()
        print(f"Created {len(items)} items")
        
        print("\n✅ Database seeded successfully!")
        print(f"Users: {', '.join([u.username for u in users])}")
        print(f"Items: {len(items)} tasks added")

if __name__ == '__main__':
    seed_database()
