""" DAO AsyncPG - Samuel Santos 8-Set-2019 """
import asyncio, asyncpg, os, logging
from api.library.dao.helper import make_where
from api.library.dao.configs import Operations
from typing import List

ioloop = asyncio.get_event_loop()
asyncio.set_event_loop(ioloop)
#logging.basicConfig(level=logging.DEBUG)

# DAO asyncio and postgresql
class DAOAsyncPG():

    DATABASE_USER       = None
    DATABASE_PASSWORD   = None
    DATABASE_HOST       = None
    DATABASE_PORT       = None
    DATABASE_NAME       = None

    table               = None
    pk                  = None
    result_query        = None
    sql_query           = None

    __action            = Operations.SELECT
    __limit             = None
    __offset            = None
    __columns           = None
    __where             = None
    __order             = None
    __sets              = None
    __values            = None
    __conflicts         = None
    __group             = None
    __lefts             = None
    __rights            = None
    __inners            = None

    __conn              = None
    __strconnection     = None

    def __init__(self):

        data_connection = ['DATABASE_USER', 'DATABASE_PASSWORD', 'DATABASE_HOST', 'DATABASE_PORT', 'DATABASE_NAME']
        for key in data_connection:
            setattr(self, key, os.environ.get(key, None))
            if getattr(self, key) == None :
                raise Exception("Environment variable {} is None".format(key)) 

        taskConn = asyncpg.connect(
            user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
            database=self.DATABASE_NAME, host=self.DATABASE_HOST )

        self.__conn = asyncio.get_event_loop().run_until_complete(taskConn)
        
    async def connect(self):
        if self.__conn == None:
            taskConn = await asyncpg.connect(
                user=self.DATABASE_USER, password=self.DATABASE_PASSWORD,
                database=self.DATABASE_NAME, host=self.DATABASE_HOST )
            self.__conn = taskConn
            return self.__conn
        return self.__conn
        
    def close(self):
        r = self.__conn.close()
        return r




    def get_query(self):
        if self.__action != Operations.INSERT_AND_UPDATE :
            self.__raw_sql()
        else:
            self.__raw_sql_update_or_create()

        return self.sql_query

    #*****************************************
    # basic operations on PostgreSQL
    #*****************************************
    def do(self):

        #Criar SQL
        if self.__action != Operations.INSERT_AND_UPDATE :
            self.__raw_sql()
        else:
            self.__raw_sql_update_or_create()
            
        if self.__action in [Operations.INSERT, Operations.SELECT] :

            self.result_query = asyncio.get_event_loop().run_until_complete(self.__conn.fetch( self.sql_query ))
            
            if self.result_query == None :
                return None

            if len(self.result_query) > 1 : 
                return [ dict(v) for v in self.result_query ]
            elif len(self.result_query) == 1 : 
                return dict(self.result_query[0])
            else: 
                return None
            
        elif self.__action in [ Operations.UPDATE, Operations.INSERT_AND_UPDATE ] :

            self.result_query = asyncio.get_event_loop().run_until_complete(self.__conn.execute( self.sql_query ))
            
            if self.result_query == Operations.UPDATE.value + ' 0':
                self.result_query  = None

        return self.result_query
        
    def execute_list(self, sql):
        
        self.result_query = asyncio.get_event_loop().run_until_complete(self.__conn.fetch( sql ))

        if self.result_query == None :
            return None

        if len(self.result_query) > 0 : 
            return dict(self.result_query[0])

        return None

    def execute(self, sql):

        self.result_query = asyncio.get_event_loop().run_until_complete(self.__conn.fetch( sql ))
        if len(self.result_query) > 1 : 
            return [ dict(v) for v in self.result_query ]
        elif len(self.result_query) == 1 : 
            return dict(self.result_query[0])
        else: 
            return None

    def first(self):
        self.do()
        if len(self.result_query) > 0 : 
            return dict(self.result_query[0])
        return None

    def list(self):
        self.do()
        if len(self.result_query) > 0 : 
            return [ dict(v) for v in self.result_query ]
        return None



    #*****************************************
    # JOINS
    #*****************************************
    def inner_join(self, model, **on):
        self.inners = { "model" : model, "on" : on }
        return self
    
    def left_join(self, model, **on):
        self.lefts = { "model" : model, "on" : on }
        return self

    def right_join(self, model, **on):
        self.rights = { "model" : model, "on" : on }
        return self


    #*****************************************
    # Basic filters, orders ...
    #*****************************************
    def group_by(self, group: List[str]):
        self.__group = group
        return self

    def order_by(self, order: dict):
        self.__order = order
        return self

    def filter(self, where: dict):
        self.__where = where
        return self

    def limit_offset(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset
        return self



    #*****************************************
    # Basic actions 
    #*****************************************
    def select(self, limit: str=None, offset: str=None, *, columns=None, where=None, order=None):
        self.__action     = Operations.SELECT
        self.__columns    = columns
        self.__where      = where
        self.__order      = order 
        self.__limit      = limit 
        self.__offset     = offset
        return self
    
    def update(self, limit: str=None, offset: str=None, *, sets=None, where=None, order=None):
        self.__action     = Operations.UPDATE
        self.__sets       = sets
        self.__where      = where
        self.__order      = order 
        self.__limit      = limit 
        self.__offset     = offset
        return self

    def delete(self, limit: str=None, offset: str=None, *, where=None, order=None):
        self.__action     = Operations.DELETE
        self.__where      = where
        self.__order      = order 
        self.__limit      = limit 
        self.__offset     = offset
        return self

    def insert(self, values=None):
        self.__action     = Operations.INSERT
        self.__values     = values
        return self

    def update_or_create(self, conflicts, values):
        self.__action     = Operations.INSERT_AND_UPDATE
        self.__values     = values
        self.__conflicts  = conflicts
        return self




    #*****************************************
    # Create SQL string
    #*****************************************
    def __raw_sql_update_or_create(self):

        #self.__values = filter(None, self.__values)

        _conflicts = ",".join(self.__conflicts)
        if type(self.__values) == list :
            _updates     = [ "{}=EXCLUDED.{}".format(key, key) for key, value in self.__values[0].items() ]
            _columns     = [ "{}".format(key) for key, value in self.__values[0].items() ]
            _values_insert = ",".join([ "(" + ",".join( "'{}'".format(v) if v is not None else 'NULL' for k, v in inserts.items() ) + ")" for inserts in self.__values ])
        else:
            _updates     = [ "{}=EXCLUDED.{}".format(key, key) for key, value in self.__values.items() ]
            _columns     = [ "{}".format(key) for key, value in self.__values.items() ]
            _values_insert     = "(" + ",".join([  "'{}'".format(value) if value is not None else 'NULL' for key, value in self.__values.items() ]) + ")"

        self.__action = Operations.INSERT_AND_UPDATE
        self.sql_query = '''INSERT INTO {} ({})
                VALUES {}
                ON CONFLICT ({}) 
                DO UPDATE 
                SET {}'''.format( self.table , ",".join(_columns), _values_insert, _conflicts, ",".join(_updates))


    def __raw_sql(self):
        
        if self.__action != Operations.INSERT:
            _columns    = ",".join(self.__columns) if self.__columns != None else '*'
            _order      = ",".join( '{} {}'.format(col, val) for col, val in self.__order.items() ) if self.__order != None else None
            _group      = ",".join( ' {} '.format(col) for col in self.__group ) if self.__group != None else None
            _where      = " AND ".join([ make_where(key, value) for key, value in self.__where.items() ]) if self.__where != None else None
            _limit      = "LIMIT {} OFFSET {}".format( str(self.__limit), str(self.__offset)) if self.__limit != None else None
            
            _sql_query = ''
            
            if self.__action == Operations.SELECT :
                _sql_query  = '''{} {} FROM {} '''.format(self.__action.value, _columns, self.table )
            elif self.__action == Operations.DELETE :
                _sql_query  = '''{} FROM {} '''.format(self.__action.value, self.table)
            elif self.__action == Operations.UPDATE :
                _sql_query  = '''{} {} '''.format(self.__action.value, self.table)
                _sets       = ",".join( [ "{}='{}'".format(key, value) for key, value in self.__sets.items()  ] ) if self.__sets != None else None
                _sql_query  = _sql_query + ''' SET {} '''.format(_sets) if _sets != None else _sql_query
            else:
                raise 'Type: action "{}" was not recognized'.format(self.__action.__str__)

            _sql_query  = _sql_query + ''' WHERE {} '''.format(_where) if _where != None else _sql_query
            _sql_query  = _sql_query + ''' GROUP BY {}'''.format(_group) if _group != None else _sql_query
            _sql_query  = _sql_query + ''' ORDER BY {}'''.format(_order) if _order != None else _sql_query
            _sql_query  = _sql_query + _limit if _limit != None else _sql_query

        elif self.__action == Operations.INSERT:

            if type(self.__values) == list :
                _columns_insert    = ",".join([ "{}".format(key) for key, value in self.__values[0].items() ])
                _values_insert = ",".join([ "(" + ",".join( "'{}'".format(v) if v is not None else 'NULL' for k, v in inserts.items() ) + ")" for inserts in self.__values ])
            else:
                _columns_insert    = ",".join([ "{}".format(key) for key, value in self.__values.items() ])
                _values_insert     = "(" + ",".join([ "'{}'".format(value) if value is not None else 'NULL' for key, value in self.__values.items() ]) + ")"

            _sql_query  = '''{} INTO {} ({}) VALUES {} '''.format(self.__action.value, self.table, _columns_insert, _values_insert)

            if self.pk != None :
                _sql_query = _sql_query + " RETURNING {} ".format(self.pk)
        
        else:

            raise 'Type: action "{}" was not recognized'.format(self.__action.__str__)
        
        self.sql_query = _sql_query