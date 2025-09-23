from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User
from schemas import UserResponse, UserCreate, Token, UserLogin
from auth import (
        hash_password,
        authenticate_user,
        ACCESS_TOKEN_EXPIRE_MINUTES,
        create_access_token,
        )

app = FastAPI(title="Password Manager")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return HTMLResponse("""
                        <html>
                            <head>
                                <title>Password Manager</title>
                            </head>
                            <body>
                                <h1>Password Manager</h1>
                                <p>Server is running!</p>
                            </body>
                        </html>
                        """)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running!"}

# Auth endpoints
@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Register a new user
    print(user_data)
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
                )

    # Create new user
    hashed_password = hash_password(user_data.password)
    hashed_master_password = hash_password(user_data.master_password)

    new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            master_key=hashed_master_password
            )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/api/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Authenticate user and return JWT
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                )

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
            )

    return {"access_token": access_token, "token_type": "bearer"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
