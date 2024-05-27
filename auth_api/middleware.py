from django.utils.deprecation import MiddlewareMixin


class AttachAuthTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_token = request.COOKIES.get('access_token')
        if auth_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
