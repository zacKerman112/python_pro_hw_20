import logging
from django.http import HttpResponseNotFound, HttpResponseServerError


logger = logging.getLogger(__name__)


class AccessControlLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in [401, 403] or (request.path.startswith('/admin/') and not request.user.is_authenticated):
            user_info = request.user if request.user.is_authenticated else "Анонімний користувач"
            ip_address = request.META.get('REMOTE_ADDR')
            
            logger.warning(
                f"Спроба несанкціонованого доступу! "
                f"Користувач: {user_info} | IP: {ip_address} | URL: {request.path}"
            )
            
        return response


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        response['Server'] = 'Protected-Server-Enterprise'

        if response.status_code == 404:
            logger.info(f"Помилка 404: Сторінку {request.path} не знайдено.")
            
        return response


    def process_exception(self, request, exception):
        logger.error(
            f" Крах сервера (Помилка 500) на URL: {request.path} | "
            f"Помилка: {exception}", 
            exc_info=True
        )

        return None
    

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Server'] = 'Protected-Web-Server'
        response['Content-Security-Policy'] = "default-src 'self';"
        return response    