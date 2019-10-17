import json
import tornado.web
from api.models.user import User
from api.library.response.handler import HttpHandler
from api.library.security.authentication import Authentication

class Users(HttpHandler):

    async def get(self):
        """
        ---
        tags:
        - Users
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
        self.response(self.request.user)

    async def post(self):
        """
        ---
        tags:
        - Users
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
        
        user    = User()

        senha   = User.encrypt('senha1234')
        salt    = user.salt

        user    = User().insert(values={"password":senha, "username":"user", "salt":salt}).do()
        
        self.response( json.dumps( user ) )

    async def put(self):
        """
        ---
        tags:
        - Users
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

        user    = User().select().where(where={ "username" : "user" }).first()
        if User.match_password(user=user, password='senha1234') : 
            token = await Authentication().get_token(user=user)

        self.response( json.dumps( { "token" : token } ) )