from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI, api_controller, http_post, permissions
from ninja_jwt.schema import TokenObtainPairInputSchema
from ninja_jwt.tokens import RefreshToken
from typing import Dict, Any, Type
from django.contrib.auth import authenticate
from ninja.errors import HttpError

class CustomTokenObtainPairSerializer(TokenObtainPairInputSchema):
    email: str

    def validate(self) -> Dict[str, Any]:
        # Authenticate user using the provided credentials
        # TokenObtainPairInputSchema has fields from the model usually, assuming username/password
        # We access fields via self.field_name (Pydantic model)
        
        user = authenticate(username=self.username, password=self.password)
        
        if user is None:
            # Check if active? authenticate checks IS_ACTIVE usually?
            # actually authenticate verifies password.
            # If default backend is used.
            raise HttpError(401, "No active account found with the given credentials")
        
        if not user.is_active:
             raise HttpError(401, "User is inactive")
        
        self._user = user

        if self._user.email != self.email:
            raise HttpError(401, "Email address does not match the username.")

        # Re-generate token to ensure claims are added
        refresh = RefreshToken.for_user(self._user)
        refresh['role'] = self._user.role
        refresh['username'] = self._user.username
        refresh['email'] = self._user.email

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        
        # Add extra response data if needed
        data["role"] = self._user.role
        data["username"] = self._user.username
        data["email"] = self._user.email
        return data

@api_controller("/auth", tags=["Auth"])
class CustomNinjaJWTController(NinjaJWTDefaultController):
    auto_import = False  # Disable auto import to avoid conflicts if needed

    @http_post("/login", response={200: dict}, auth=None)
    def obtain_token(self, user_token: CustomTokenObtainPairSerializer):
        return user_token.validate()