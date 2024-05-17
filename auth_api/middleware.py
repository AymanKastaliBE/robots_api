from django.utils.deprecation import MiddlewareMixin


class AttachAuthTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_token = request.COOKIES.get('auth_token')
        if auth_token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth_token}'
