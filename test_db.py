from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Password
import bcrypt

def test_database():
    # Create a database session
    db = SessionLocal()

    try:
        # Create a user
        print("Testing user creation...")

        # Hash a password
        password = "testpassword"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
                email="test@proton.me",
                hashed_password=hashed.decode('utf-8'),
                master_key="temporary_key"
                )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"Created user with ID: {new_user.id}")

        # Create a password entry
        print("Testing password creation...")

        new_password = Password(
                user_id=new_user.id,
                service_name="Gmail",
                username="test@gmail.com",
                encrypted_password="encrypted_testpassword",

                url="https://mail.google.com",
                notes="Test notes"
                )

        db.add(new_password)
        db.commit()

        print(f"Created password entry with ID: {new_password.id}")

        # Query data
        print("Testin queries...")

        user = db.query(User).filter(User.email == "test@gmail.com").first()
        print(f"Found user: {user.email}, created: {user.created_at}")

        # Find passwords for the user
        user_passwords = db.query(Password).filter(Password.user_id == user.id).all()
        print(f"User has {len(user_passwords)} password entries.")

        for pwd in user_passwords:
            print(f"Service: {pwd.service_name}, Username: {pwd.username}")

            print("All tests passed!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally: 
        db.close()

if __name__ == "__main__":
    test_database()
