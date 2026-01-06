from ninja_extra import api_controller, route
from ninja import Form, Schema
from typing import List

from ninja_jwt.tokens import RefreshToken

from .models import User
from .schemas import TokenResponse, ErrorResponse
from .views import generate_uni_id


class UserIdsSchema(Schema):
    user_ids: List[int]


@api_controller("/auth", tags=["Auth"])
class UserController:

    # ----------------------------
    # Fetch Users by IDs
    # ----------------------------
    @route.post("/get_users")
    def get_users(self, request, payload: UserIdsSchema):
        users = User.objects.filter(id__in=payload.user_ids)
        return [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
            }
            for u in users
        ]

    # ----------------------------
    # Register User
    # ----------------------------
    @route.post(
        "/register",
        response={200: TokenResponse, 400: ErrorResponse},
    )
    def register(
        self,
        request,
        password: str = Form(...),
        email: str = Form(...),
        role: str = Form(...),
    ):
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
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        # Custom claims
        refresh["role"] = user.role
        refresh["username"] = user.username
        refresh["email"] = user.email

        return {
            "access_token": str(refresh.access_token),
            "user_id": str(user.username),
            "userId": user.id,
            "role": user.role,
        }
