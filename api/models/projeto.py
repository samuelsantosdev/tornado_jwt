from api.library.dao.core import DAOAsyncPG

class Projeto(DAOAsyncPG):
    
    def __init__(self):
        self.table   = 'public.words'
        self.pk      = 'id'