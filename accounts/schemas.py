from ninja import Schema

class RegisterSchema(Schema):
    email: str
    password: str
    role: str


class TokenResponse(Schema):
    access_token: str
    user_id: str
    userId : int
    role: str

class ErrorResponse(Schema):
    error: str