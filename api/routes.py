from .controllers.welcome import WordsHandler
from .controllers.users import *
import tornado

def get_routes():
    return [
        tornado.web.url(r"/", tornado.web.RedirectHandler, dict(url=r"/api/doc")),
        tornado.web.url(r"/api/v1/words", WordsHandler),
        tornado.web.url(r"/api/v1/users", Users),
    ]