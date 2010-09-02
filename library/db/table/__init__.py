#!/usr/bin/env python
# -*- coding: utf-8 -*-

class result:

    __attribute = None

    def factory(self, result):
        for row in result:
            setattr(self, '_'+ row.keys()[0], row.values()[0])
        return self

    def __getattr__(self, name):
        self.__attribute = '_' + name[4: len(name)]
        return getattr(self, '__methodmissing__')

    def __methodmissing__(self, *args, **kwargs):
        return eval('self.' + self.__attribute)

class abstract:

    __attributes = []
    __result = []
    __resultset = []
    __pkey = None
    __table = None
    __database = None

    def __init__(self, database, table, pkey):

        self.__attributes = []
        self.__database = database
        self.__table = table
        self.__pkey = pkey

        self.__database.query('SELECT a.attname \
                FROM pg_class c, pg_attribute a, pg_type t \
                WHERE c.relname = \'%s\' \
                AND a.attnum > 0 \
                AND a.attrelid = c.oid \
                AND a.atttypid = t.oid' % (self.__table))
        
        for row in self.__database.getrows():
            self.__attributes.append(row[0])

    def select(self, key):
        self.__result = []
        self.__database.query('SELECT * FROM %s WHERE %s = %s' % 
                (self.__table, 
                 self.__pkey,
                 key) )

        idx = 0
        for col in self.__database.getrows()[0]:
            self.__result.append({self.__attributes[idx]: col})
            idx = idx + 1

    def selectall(self):

        resultset = []
        self.__result = []
        self.__database.query('SELECT * FROM %s' % (self.__table) )
        for rows in self.__database.getrows():
            idx = 0
            for col in rows:
                self.__result.append({self.__attributes[idx]: col})
                idx = idx + 1

            res = result()
            data = res.factory(self.__result)
            self.__result = []
            resultset.append(data)

        self.__resultset = resultset

    def selectby(self, where):
        resultset = []
        self.__result = []
        if not isinstance(where, type(where)):
            raise Exception, 'WHERE clause must be a list'

        if len(where) > 1:
            query = 'SELECT * FROM %s WHERE %s ' % (self.__table, where[0])
            where.pop(0)
            for cond in where:
                query = query + ' AND %s' % (cond)
        else:
            query = 'SELECT * FROM %s WHERE %s' % (self.__table, where[0]) 

        self.__database.query(query)
        for rows in self.__database.getrows():
            idx = 0
            for col in rows:
                if col == '': col = None 
                self.__result.append({self.__attributes[idx]: col})
                idx = idx + 1

            res = result()
            data = res.factory(self.__result)
            self.__result = []
            resultset.append(data)

        self.__resultset = resultset

    def execute(self, query):
        self.__result = []
        self.__database.query(query)

        idx = 0
        for col in self.__database.getrows()[0]:
            self.__result.append({self.__attributes[idx]: col})
            idx = idx + 1

    def getresultset(self):
        return self.__resultset

    def getresult(self):
        res = result()
        ret  = res.factory(self.__result)
        return ret


