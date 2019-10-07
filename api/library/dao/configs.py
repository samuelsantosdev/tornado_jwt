from enum import Enum

class Operations(Enum):
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    SELECT = 'SELECT'
    DELETE = 'DELETE'
    INSERT_AND_UPDATE = 'INSERT_AND_UPDATE'