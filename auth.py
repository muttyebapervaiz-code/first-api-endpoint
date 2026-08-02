from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()
bearer = HTTPBearer()

class AuthData(BaseModel):
    email: str
    password: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    result = supabase.auth.get_user(token)
    if not result or not result.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result.user

@router.post("/auth/signup", status_code=201)
def signup(data: AuthData):
    result = supabase.auth.sign_up({"email": data.email, "password": data.password})
    if not result.user:
        raise HTTPException(status_code=400, detail="Signup failed")
    return {"message": "Signup successful", "user_id": result.user.id}

@router.post("/auth/login")
def login(data: AuthData):
    result = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    if not result.user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": result.session.access_token, "token_type": "bearer"}

@router.post("/auth/logout", status_code=204)
def logout(user=Depends(get_current_user)):
    supabase.auth.sign_out()

@router.get("/protected/profile")
def profile(user=Depends(get_current_user)):
    return {"user_id": str(user.id), "email": user.email}

@router.get("/public/info")
def public_info():
    return {"message": "This is public info, no login needed"}