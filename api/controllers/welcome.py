import json
import tornado.web
from api.models.projeto import Projeto
from api.models.user import User
from api.library.response.handler import HttpHandler
from api.library.security.authentication import Authentication

class WordsHandler(HttpHandler):

    @HttpHandler.login_required
    async def get(self):
        """
        ---
        tags:
        - Welcome
        summary: Get posts details
        description: posts full version
        produces:
        - application/json
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to return
            required: true
            type: string
        responses:
            200:
              description: list of posts
        """
        response = { 'token' : 1 }
        return self.response( response )