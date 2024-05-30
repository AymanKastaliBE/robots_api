from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.conf import settings as django_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class AttachAuthTokenMiddleware(MiddlewareMixin):
    jwt_authentication = JWTAuthentication()
    @staticmethod
    def is_access_token_valid(access_token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(access_token)
            return True
        except InvalidToken:
            return False

    @staticmethod
    def is_refresh_token_valid(refresh_token):
        try:
            RefreshToken(refresh_token)
            return True
        except TokenError:
            return False

    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        # username = request.COOKIES.get('username')
        
        is_access_token_valid = self.is_access_token_valid(access_token)
        is_refresh_token_valid = self.is_refresh_token_valid(refresh_token)
        
        if access_token and is_access_token_valid:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            # request.username = username
            try:
                user, _ = self.jwt_authentication.authenticate(request)
                if user is not None:
                    request.user = user
            except InvalidToken:
                pass
        elif not access_token or not is_access_token_valid:
            if refresh_token and is_refresh_token_valid:
                try:
                    refresh = RefreshToken(refresh_token)
                    access_token = str(refresh.access_token)
                    
                    access_token_expiration = datetime.now() + django_settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                    request.access_token = access_token
                    request.access_token_expiration = access_token_expiration
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                    # request.username = username
                    try:
                        user, _ = self.jwt_authentication.authenticate(request)
                        if user is not None:
                            request.user = user
                    except InvalidToken:
                        pass
                except TokenError as e:
                    print(f'Refresh token error: {e}')
                except Exception as e:
                    print(f'Unexpected error: {e}')

    def process_response(self, request, response):
        if hasattr(request, 'access_token'):
            response.set_cookie('access_token', request.access_token, expires=request.access_token_expiration, httponly=True)
        return response
    