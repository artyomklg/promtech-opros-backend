from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from httpx_oauth.clients.google import GoogleOAuth2

from .manager import get_user_manager
from .models import User
from ..config import settings

cookie_transport = CookieTransport(
    cookie_name="access_token", cookie_max_age=3600)

# google_oauth_client = GoogleOAuth2(
#     settings.GOOGLE_OAUTH_CLIENT_ID,
#     settings.GOOGLE_OAUTH_CLIENT_SECRET
# )


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
