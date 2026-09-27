from sqlalchemy.orm import Session

from app.core.errors import ConflictError, UnauthorizedError
from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories import users
from app.schemas.auth import RegisterRequest


def register_user(db: Session, payload: RegisterRequest) -> User:
    email = str(payload.email).lower()
    if users.get_by_email(db, email):
        raise ConflictError("Já existe um usuário com este e-mail.")

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        role=UserRole.MORADOR,
        neighborhood=payload.neighborhood,
        organization=payload.organization,
    )
    return users.save(db, user)


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = users.get_by_email(db, email.lower())
    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError()
    return user
