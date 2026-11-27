from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user import UserRead


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    neighborhood: str | None = Field(default=None, max_length=120)
    organization: str | None = Field(default=None, max_length=160)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(character.isdigit() for character in value):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not any(character.isalpha() for character in value):
            raise ValueError("A senha deve conter pelo menos uma letra.")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class AuthUserResponse(UserRead):
    model_config = ConfigDict(from_attributes=True)
