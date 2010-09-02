import db.pgsql

class adapter:

    __adapter = None

    def __init__(self, dbtype):
        if dbtype == 'pgsql':
            self.__adapter = db.pgsql.adapter()

    def getAdapter(self):
        return self.__adapter
