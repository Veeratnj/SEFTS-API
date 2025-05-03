from sqlalchemy.orm import Session
from app.models.models import User, LoginTrack
from datetime import datetime, timedelta
import jwt
import os

SECRET_KEY = os.getenv("LOGIN_SECRET_KEY", "your-secret-key")  # Replace with a secure key
ALGORITHM = "HS256"

def authenticate_user(email: str, password: str, db: Session) -> dict:
    """
    Authenticate the user by verifying the email and password, and create a login token.

    :param email: User's email
    :param password: User's password
    :param db: Database session
    :return: User details and token if authentication is successful, otherwise None
    """
    # Search for the user in the database
    print('email',email)
    print('password',password)  
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        return None

    # Generate a JWT token
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "role":user.role,
        "exp": datetime.utcnow() + timedelta(hours=12)  # Token expires in 12 hour
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Insert login details into the login_track table
    login_track = LoginTrack(
        user_id=user.id,
        token=token,
        login_time=datetime.utcnow(),
        ip_address="0.0.0.0",  # Replace with actual IP address
        device_info="Unknown Device"  # Replace with actual device info
    )
    db.add(login_track)
    db.commit()

    # Return user details and token
    return {
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        "role":user.role,
        'token': token,
    }