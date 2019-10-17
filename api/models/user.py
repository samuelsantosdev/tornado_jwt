from api.library.dao.core import DAOAsyncPG
import hashlib, binascii, random, string

class User(DAOAsyncPG):

    salt        = None
    pk          = 'id'
    table       = 'public.auth_users' # schema.table

    def __make_salt(self):
        base = ''.join(random.sample(string.ascii_lowercase, 64))
        self.salt = hashlib.sha1(str(base).encode('utf-8')).hexdigest()

    @classmethod    
    def encrypt(self, value, salt=None):
        
        self.salt = self.__make_salt(value) if salt == None else salt

        dk = hashlib.pbkdf2_hmac('sha256', value.encode('UTF-8'), self.salt.encode('UTF-8'), 100000)
        return str(binascii.hexlify(dk), 'utf-8')

    @classmethod    
    def match_password(self, user, password):
        enc1 = self.encrypt(password, user['salt'])
        return enc1 == user['password']
        
