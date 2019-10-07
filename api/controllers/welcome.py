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
        - Posts
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
              schema:
                $ref: '#/definitions/PostModel'
        """
        #json_response = json.dumps({'data':['1']})
        #senha   = User.encrypt('senha1234')
        
        #salt    = User.salt
        #user    = await User().insert(values={"password":senha, "username":"user", "salt":salt}).do()
        #json_response = user

        #user    = await User().select().where(where={ "username" : "user" }).first()
        #if User.match_password(user=user, password='senha1234') : 
        #    token = await Authentication().get_token(user=user)

        return self.response( json.dumps( { 'token' : 1 } ) )