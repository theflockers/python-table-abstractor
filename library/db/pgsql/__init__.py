import psycopg2 as pg

class db_exception(Exception):
    pass

class adapter:
 
    __dbname  = None
    __dbuser  = None
    __dbpass  = None
    __dbhost  = None
    __dbport  = 5432
    __conn    = None
    __model   = None
    __rows    = None

    def factory(self, dbuser, dbpass, dbname, dbhost, dbport=5432):
        __model = adapter()
        __model.__setDBName(dbname)
        __model.__setDBUser(dbuser)
        __model.__setDBPass(dbpass)
        __model.__setDBHost(dbhost)
        __model.__setDBPort(dbport)

        __model.__connect()

        return __model

    def __connect(self):
        self.__conn = pg.connect(user=self.__dbuser, 
                                 password=self.__dbpass, 
                                 host=self.__dbhost,
                                 port=self.__dbport, 
                                 database=self.__dbname)

    def query(self, query):
        cur = self.__conn.cursor()
        cur.execute(query)
        self.__rows = cur.fetchall()
        cur.close()

    def getrows(self):
        return self.__rows;

    def __setDBName(self, dbname):
        self.__dbname = dbname

    def __setDBUser(self, dbuser):
        self.__dbuser = dbuser

    def __setDBPass(self, dbpass):
        self.__dbpass = dbpass

    def __setDBHost(self, dbhost):
        self.__dbhost = dbhost

    def __setDBPort(self, dbport):
        self.__dbport = dbport
