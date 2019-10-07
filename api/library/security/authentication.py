from datetime import datetime, timedelta
import jwt, os, http
from api.models.user import User
import tornado

class Authentication():

    async def get_token(self, user):
        
        payload = {
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(seconds=int(os.environ.get('JWT_EXP_DELTA_SECONDS')))
        }

        jwt_token = jwt.encode(payload, os.environ.get('JWT_SECRET'), os.environ.get('JWT_ALGORITHM'))
        return jwt_token.decode('utf-8')

async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, os.environ.get('JWT_SECRET'),
                                    algorithms=[os.environ.get('JWT_ALGORITHM')])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                raise Exception('Token is invalid')

            request.user = User().select().where(where={id : payload['user_id']}).first()
        return await handler(request)
    return middleware