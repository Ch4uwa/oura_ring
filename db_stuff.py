"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com

Setup database
"""
import sqlite3
import json


class DataBaseOura:
    def __init__(self, db_name='db_oura.db'):
        self.db_name = db_name
        self.conn = None

    def db_connect(self):
        # Start a connection to db file
        try:
            with sqlite3.connect(self.db_name) as conn:
                self.conn = conn
                print('Connection to {}'.format(self.db_name))
        except sqlite3.Error as e:
            print('sqlite3 Error: {}'.format(e))
        except Exception as e_all:
            print('Exception: {}'.format(e_all))

    def create_table(self, sql_script=None, sql=None):
        if sql_script is not None:
            with self.conn:
                self.conn.executescript(sql_script)
                print('script')
        if sql is not None:
            with self.conn:
                self.conn.execute(sql=sql)
        if sql_script is None and sql is None:
            print('nothing to execute')

    def db_query(self):
        self.db_connect()
        # Select all from table
        with self.conn:
            cur = self.conn.cursor()
            return cur

    def get_tables(self):
        query_tables = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        with self.conn:
            tables = self.conn.execute(query_tables)
            return tables

    def insert_into(self, email=None, oura_token=None):
        if oura_token is not None:
            try:
                token_json = json.dumps(oura_token)
                self.conn.execute('INSERT INTO oura_token(token) VALUES (?)', (token_json,))

            except Exception as db_exception:
                print(db_exception)
            finally:
                self.conn.commit()
        with self.conn:
            pass

    # self.conn.execute()

    # self.conn.execute("INSERT INTO oura_token(Id, token) VALUES (?,?)", (email, o_token))

    # def update_table(self, *args):
    #     query = '''UPDATE ?
    #                SET ? = ?,
    #                column_name2 = value
    #                WHERE condition'''


def main():
    pass
    # d = DataBaseOura()
    # d.db_connect()
    # tables = d.get_tables()
    # a, b = tables.fetchall()
    # print(a)
    # print(b)
    # query = 'SELECT * FROM oura_token, oura_data'
    # x = d.db_query(query)
    # for f in x.description:
    #     print(f[0])

    # with open('dbscript/create.sql') as create:
    #
    #     d.create_table(sql_script=create.read())


if __name__ == "__main__":
    main()
