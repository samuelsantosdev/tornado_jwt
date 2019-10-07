import tornado.ioloop
import tornado.web
import os
from api.routes import get_routes
from tornado_swagger.setup import setup_swagger

#def start_app():
#    return tornado.web.Application(get_routes())
class Application(tornado.web.Application):
    _routes = get_routes()

    def __init__(self):
        setup_swagger(self._routes)
        super(Application, self).__init__(self._routes)

if __name__ == "__main__":
    app = Application()
    app.listen(os.environ.get('WS_PORT', '8080'))
    tornado.ioloop.IOLoop.current().start()
