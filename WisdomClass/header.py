from django.utils.deprecation import MiddlewareMixin

class HttpResponseCustomHeader(MiddlewareMixin):
    def process_response(self, request, response):
        if not response.has_header("Version"):
            response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response
