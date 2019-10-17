from tornado.web import RequestHandler
import settings

class HttpHandler(RequestHandler):

    user = None

    def set_default_headers(self, *args, **kwargs):

        self.set_header("Access-Control-Allow-Origin", ','.join(settings.MS_ALLOW_ORIGIN))
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", ','.join(settings.MS_ALLOW_METHODS))
        
    def response(self, json: str, status: int=200):

        self.clear()
        self.write( json )
        self.set_status(status)
        self.set_header("Content-Type", "application/json")

    def login_required(func):
        def wrapper(request):
            if not request.user:
                raise Exception("Login required", 401)
            return func(request)
        return wrapper