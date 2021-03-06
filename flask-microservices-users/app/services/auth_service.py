from flask_jwt_extended import create_access_token, create_refresh_token

from app.exceptions.http_exceptions import BadCredentialsException
from app.repositories.user_repository import UserRepository
from app.security.current_user import CurrentUser
from app.security.security_utils import SecurityUtils


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate(self, email, password):
        user = self.user_repository.get_user_by_email(email)

        if not user or not user.verify_password(password):
            raise BadCredentialsException('Email or password incorrect')

        current_user = CurrentUser.from_user(user)

        return {
            'access_token': create_access_token(identity=current_user),
            'refresh_token': create_refresh_token(identity=current_user)
        }

    def refresh_token(self):
        current_user = SecurityUtils.get_current_user()

        return {
            'access_token': create_access_token(identity=current_user),
            'refresh_token': create_refresh_token(identity=current_user)
        }
