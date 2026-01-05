from ninja import Router, Form, File, Schema
from .models import User
from ninja_jwt.tokens import RefreshToken
from .schemas import RegisterSchema, TokenResponse, ErrorResponse
from .views import generate_uni_id
from typing import List

app = Router()

class UserIdsSchema(Schema):
    user_ids: List[int]

@app.post("/get_users")
def get_users(request, payload: UserIdsSchema):
    users = User.objects.filter(id__in=payload.user_ids)
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email
        }
        for u in users
    ]

@app.post("/register", response={200: TokenResponse, 400: ErrorResponse})
def register(request, password: str = Form(...),
    email: str = Form(...),
    role: str = Form(...)):
    if User.objects.filter(email=email).exists():
        return 400, {"error": "User already exists"}
    
    while True:
        username = generate_uni_id(role)
        if not User.objects.filter(username=username).exists():
            break

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role
    )

    refresh = RefreshToken.for_user(user)
    
    # Add custom claims
    refresh["role"] = user.role
    refresh["username"] = user.username
    refresh["email"] = user.email

    print(user.username)
    return {
        "access_token": str(refresh.access_token),
        "user_id": str(user.username),
        "userId": user.id,
        "role": user.role
    }