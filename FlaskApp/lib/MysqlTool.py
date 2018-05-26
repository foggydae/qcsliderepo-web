# -*- coding:utf-8 -*-
import MySQLdb

class MysqlTool:
    def __init__(self, db_name, db_ip, db_port, db_user, db_password):
        self.__db_name = db_name
        self.__db_ip = db_ip
        self.__db_port = db_port
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db = MySQLdb.connect(host=db_ip, port=db_port, user=db_user, passwd=db_password, db=db_name)
        self.__cursor = self.__db.cursor()
        self.__db.set_character_set('utf8')

    def __del__(self):
        self.__db.close()

    def getLength(self, table, date):
        query_sql = 'select count(*) from %s where trade_dt >= %s ;'
        try:
            self.__cursor.execute(query_sql % (table, date))
            results = self.__cursor.fetchall()
            return results[0][0]
        except MySQLdb.Error as e:
            try:
                print("Error %d:\n%s" % (e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error:%s" % str(e))
            self.__db.rollback()

    def insert(self, table ,dataList):
        insert_sql = 'insert into %s'% table + ' values(%s);'
        try:
            argList = ','.join(['%s'] * len(dataList))
            self.__cursor.execute(insert_sql % argList, dataList)
            self.__db.commit()
        except MySQLdb.Error as e:
            try:
                print("Error %d:\n%s" % (e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error:%s" % str(e))
            self.__db.rollback()

    def selectAll(self, table):
        query_sql = 'select * from %s;' % (table)
        try:
            self.__cursor.execute(query_sql)
            results = self.__cursor.fetchall()
            print(results)
            return results
        except MySQLdb.Error as e:
            try:
                print("Error %d:\n%s" % (e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error:%s" % str(e))
            self.__db.rollback()