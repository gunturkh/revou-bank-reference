from werkzeug.security import generate_password_hash
import uuid

# Import app and db after they are properly initialized
from app import app
from db import User, Account, Transaction, db

def init_db():
    """Initialize the database with some test data"""
    print("Starting database initialization...")
    
    # Reset the database
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("Creating test users...")
        
        # Create test users
        test_user1 = User(
            username="johndoe",
            email="john.doe@example.com",
            password=generate_password_hash("password123"),
            first_name="John",
            last_name="Doe"
        )
        
        test_user2 = User(
            username="janedoe",
            email="jane.doe@example.com",
            password=generate_password_hash("password123"),
            first_name="Jane",
            last_name="Doe"
        )
        
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.commit()
        
        print("Creating test accounts...")
        
        # Create test accounts
        account1 = Account(
            account_number=f"ACC-{uuid.uuid4().hex[:8].upper()}",
            account_type="savings",
            balance=5000.0,
            user_id=test_user1.id
        )
        
        account2 = Account(
            account_number=f"ACC-{uuid.uuid4().hex[:8].upper()}",
            account_type="checking",
            balance=2500.0,
            user_id=test_user1.id
        )
        
        account3 = Account(
            account_number=f"ACC-{uuid.uuid4().hex[:8].upper()}",
            account_type="savings",
            balance=7500.0,
            user_id=test_user2.id
        )
        
        db.session.add(account1)
        db.session.add(account2)
        db.session.add(account3)
        db.session.commit()
        
        print("Creating test transactions...")
        
        # Create test transactions
        transaction1 = Transaction(
            transaction_type="deposit",
            amount=1000.0,
            to_account_id=account1.id,
            description="Initial deposit"
        )
        
        transaction2 = Transaction(
            transaction_type="withdrawal",
            amount=500.0,
            from_account_id=account1.id,
            description="ATM withdrawal"
        )
        
        transaction3 = Transaction(
            transaction_type="transfer",
            amount=750.0,
            from_account_id=account1.id,
            to_account_id=account2.id,
            description="Transfer to checking"
        )
        
        db.session.add(transaction1)
        db.session.add(transaction2)
        db.session.add(transaction3)
        db.session.commit()
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 