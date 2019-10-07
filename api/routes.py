from .controllers.welcome import WordsHandler
import tornado

def get_routes():
    return [
        tornado.web.url(r"/", tornado.web.RedirectHandler, dict(url=r"/api/doc")),
        tornado.web.url(r"/api/v1/words", WordsHandler),
    ]