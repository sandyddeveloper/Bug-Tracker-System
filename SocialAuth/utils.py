from google.auth.transport import requests
from google.oauth2 import id_token
from Auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            if "accounts.google.com" in id_info['iss']:
                return id_info
        except Exception:
            raise AuthenticationFailed("Token is invalid or has expired")



def login_social_user(email):
    user = User.objects.get(email=email)
    refresh = RefreshToken.for_user(user)
    
    return {
        'email': user.email,
        'full_name': f"{user.first_name} {user.last_name}",
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }


def register_social_user(provider, email, first_name, last_name):
    user = User.objects.filter(email=email).first()
    
    if user:
        if provider == user.auth_provider:
            return login_social_user(email)
        else:
            raise AuthenticationFailed(
                detail=f'Please continue login with {user.auth_provider}'
            )

    user_data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': settings.SOCIAL_AUTH_PASSWORD
    }
    
    new_user = User.objects.create_user(**user_data)
    new_user.auth_provider = provider
    new_user.is_verified = True
    new_user.save()

    return login_social_user(new_user.email)
