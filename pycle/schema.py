from pathlib import Path
import sqlite3

def migrate(db_path):
    # print("migrate", db_path)
    with sqlite3.connect(db_path) as conn:
        db = DB(conn)
        init_schema(db)

class DB:
    def __init__(self, conn):
        self.conn = conn

    def query(self, q, params=[]):
        cursor = self.conn.cursor()
        cursor.execute(q, params)
        return cursor.fetchall()

    def list_tables(self):
        q = "select name from sqlite_master where type='table' and name not like 'sqlite_%'"
        result = self.query(q)
        return [row[0] for row in result]

    def has_table(self, table):
        return table in self.list_tables()

def read_schema():
    p = Path(__file__).parent / "schema.sql"
    return p.read_text()

def init_schema(db):
    # print("  init_schema ...")
    if not db.has_table("env"):
        schema = read_schema()
        db.query(schema)
