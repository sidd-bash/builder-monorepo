from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from bson import ObjectId
from src.database import db
import src.models.user_model as user_models
from src.utils.auth_utils import hash_password, verify_password, create_access_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # CHANGED: Use HTTPBearer
from fastapi import Depends

# CHANGED: Use HTTPBearer for direct token input in Swagger
security = HTTPBearer() 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Signup logic (unchanged)
async def signup(user: user_models.UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({
        "$or": [
            {"email": user.email},
            {"username": user.username}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    
    # Hash password safely (SHA256 + bcrypt)
    hashed_password = hash_password(user.password)

    # Prepare user document
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    # Insert into DB
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)  # CHANGED: Use "_id" for consistency with MongoDB (instead of "id")
    return user_dict

# Login logic (unchanged)
async def login(user: user_models.UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # CHANGED: Use str(db_user["_id"]) as sub for token payload (not email) to match DB query in get_current_user
    token = create_access_token({"sub": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

# CHANGED: Adjust to use HTTPBearer dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract the raw token string
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing user ID")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert ObjectId to string for JSON serialization
    user["_id"] = str(user["_id"])
    
    # Remove sensitive fields before returning
    user.pop("hashed_password", None)
    
    return user