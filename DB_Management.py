import psycopg2
from config import config


def create_tables():
    pass


def insert_into(table):
    table = table
    pass


def connect():

    conn = None

    try:
        # set connection params
        params = config()

        # connect db serverS
        conn = psycopg2.connect(**params)

        # create cursor
        cur = conn.cursor()

        # get current db version
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        # close communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


if __name__ == '__main__':
    connect()
