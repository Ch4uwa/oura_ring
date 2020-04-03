"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com

Setup database
"""
import sqlite3
import json
import logging
from oura.ouraauth import OuraClient

logger = logging.getLogger(__name__)


class DataBaseOura:
    def __init__(self, db_name='db_oura.db'):
        self.db_name = db_name

    def db_connect(self):
        # Return a connection to db file
        # If no connection returns None
        connection = None
        try:
            with sqlite3.connect(self.db_name) as conn:
                connection = conn
                logger.info('Connection to {}'.format(self.db_name))
                return connection
        except sqlite3.Error as e:
            print('sqlite3 Error: {}'.format(e))
            logger.exception(e)
        except Exception as e_all:
            print('Exception: {}'.format(e_all))
            logger.exception(e_all)
        return connection

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

    def db_query(self, query=None):
        conn = self.db_connect()
        with conn:
            cur = conn.cursor()
            cur.execute(query)
        if cur is not None:
            cur.close()

    def get_tables(self):
        query_tables = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        with self.conn:
            tables = self.conn.execute(query_tables)
            return tables

    def insert_into(self, email=None, oura_token=None, user_info=None, sleep=None, activity=None, readiness=None):
        conn = self.db_connect()
        if email is not None and oura_token is not None:
            try:
                # using the shortcut to access the cursor through connection
                token_json = json.dumps(oura_token)
                conn.execute(
                    'INSERT INTO oura_token(Id, token) VALUES (?, ?)', (email, token_json))
                conn.commit()
            except sqlite3.Error as db_Err:
                print(db_Err)
                logger.exception(db_Err)
            except Exception as insert_exception:
                print(insert_exception)
                logger.exception(insert_exception)
            finally:
                conn.commit()
                if conn:
                    conn.close()

        if email is not None and user_info is not None and sleep is not None and activity is not None and readiness is not None:
            try:
                j_user_info = json.dumps(user_info)
                j_sleep = json.dumps(sleep)
                j_activity = json.dumps(activity)
                j_readiness = json.dumps(readiness)

                conn.execute("""INSERT INTO oura_data(Email, Personal_info, Sleep, Activity, Readiness)
                                VALUES (?,?,?,?,?)""", (email, j_user_info, j_sleep, j_activity, j_readiness))
            except sqlite3.Error as e:
                logger.exception(e)
            finally:
                conn.commit()
                conn.close()

    def get_token(self, token_id=None):
        conn = self.db_connect()

        with conn:
            cur = conn.cursor()
            cur.execute('SELECT token FROM oura_token WHERE Id = ?', (token_id,))

            r = cur.fetchone()[0]
            result = json.loads(r)

            return result

    def update_db(self, token_id, token_dict):
        # def update_table(self, *args):
        #     query = '''UPDATE ?
        #                SET ? = ?,
        #                column_name2 = value
        #                WHERE condition'''
        conn = self.db_connect()

        with conn:
            conn.execute('UPDATE oura_token SET token = (?) WHERE Id=(?)', (token_dict, token_id))

    def get_user_info(self, client_id, client_secret, access_token, refresh_token):
        client = OuraClient(client_id, client_secret, access_token, refresh_token)
        return client.user_info()


def main():
    d = DataBaseOura()
    d.get_token('1')

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
