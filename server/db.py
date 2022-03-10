from pymysql import connect
from config_basic import *

class DB(object):

    def __init__(self):
        self.conn = connect(host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD)

        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql):
        self.cursor.execute(sql)

        query_res = self.cursor.fetchone()

        if not query_res: return

        field_names = [field[0] for field in self.cursor.description] # field[0] is property name

        data_map = dict()
        for field_name, value in zip(field_names, query_res):
            data_map[field_name] = value

        return data_map

if __name__ == '__main__':
    db = DB()
    data = db.get_one("select * from user where user_name = 'u1'")
    print(data)
    db.close()