from os import path as ospath, makedirs
from psycopg2 import connect, DatabaseError

from tobrot import DOWNLOAD_LOCATION, DB_URI, LOGGER

class DatabaseManager:
    def __init__(self):
        self.err = False
        self.connect()

    def connect(self):
        try:
            self.conn = connect(DB_URI)
            self.cur = self.conn.cursor()
        except DatabaseError as error:
            LOGGER.error(f"Error in DB connection: {error}")
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_init(self):
        if self.err:
            return
        sql = """CREATE TABLE IF NOT EXISTS users (
                 uid bigint,
                 thumb bytea DEFAULT NULL
              )
              """
        self.cur.execute(sql)
        #self.cur.execute("CREATE TABLE IF NOT EXISTS {} (cid bigint, link text, tag text)".format(botname))
        self.conn.commit()
        LOGGER.info("Database Initiated")
        self.db_load()

    def db_load(self):
        # User Data
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()  # return a list ==> (uid, thumb)
        if rows:
            for row in rows:
                path = f"{DOWNLOAD_LOCATION}/thumbnails/{row[0]}.jpg"
                if row[1] is not None and not ospath.exists(path):
                    if not ospath.exists(f'{DOWNLOAD_LOCATION}/thumbnails'):
                        makedirs(f'{DOWNLOAD_LOCATION}/thumbnails')
                    with open(path, 'wb+') as f:
                        f.write(row[1])
            LOGGER.info("Users Thumb data has been imported from Database")
        self.disconnect()

    def user_save_thumb(self, user_id: int, path):
        if self.err:
            return
        image = open(path, 'rb+')
        image_bin = image.read()
        if not self.user_check(user_id):
            sql = 'INSERT INTO users (thumb, uid) VALUES (%s, %s)'
        else:
            sql = 'UPDATE users SET thumb = %s WHERE uid = %s'
        self.cur.execute(sql, (image_bin, user_id))
        self.conn.commit()
        self.disconnect()

    def user_rm_thumb(self, user_id: int, path):
        if self.err:
            return
        elif self.user_check(user_id):
            sql = 'UPDATE users SET thumb = NULL WHERE uid = {}'.format(user_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()

    def user_check(self, uid: int):
        self.cur.execute("SELECT * FROM users WHERE uid = {}".format(uid))
        res = self.cur.fetchone()
        return res

if DB_URI is not None:
    DatabaseManager().db_init()
