from fastapi import APIRouter
from src.controllers import auth_controller
import src.models.user_model as user_models
from fastapi import Depends, Security  # CHANGED: Keep Security if needed, but update dependency
from fastapi import Request

router = APIRouter()
  # CHANGED: Import Request to access request.state
@router.post("/signup", response_model=user_models.UserResponse)
async def signup_route(user: user_models.UserCreate):
    return await auth_controller.signup(user)

@router.post("/login")
async def login_route(user: user_models.UserLogin):
    return await auth_controller.login(user)

# CHANGED: Use the updated get_current_user directly (no need for oauth2_scheme)
@router.get("/me")
async def get_me(request: Request):
    user = request.state.user
    return {"user": user}