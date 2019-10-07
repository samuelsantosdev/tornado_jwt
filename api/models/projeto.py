from api.library.dao.core import model_asyncpg

@model_asyncpg
class Projeto():
    
    def __init__(self):
        self.table   = 'projetos'
        self.pk      = 'id'