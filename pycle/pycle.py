
from calendar import c
import sqlite3
import cloudpickle
import argparse
import ast
from .env import Environment
from . import schema

class Pycle:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.env = Environment(self.conn)

    def execute(self, code):
        head, tail = self._parse_code(code)
        self.do_exec(head)
        self.do_single(tail)

    def _parse_code(self, code):
        """Parses the code as ast and returns head and tail.

        The head includes all the lines except the last expr/statement and
        the tail includes the last expr/statement.

        This is done this way to run head and tail seperately to be able
        to show the output of last expression.
        """
        mod = ast.parse(code)
        head = ast.Module(mod.body[:-1], [])
        tail = ast.Interactive(mod.body[-1:])
        return head, tail

    def do_exec(self, ast_node):
        code_obj = compile(ast_node, "<input>", "exec")
        exec(code_obj, self.env)

    def do_single(self, ast_node):
        code_obj = compile(ast_node, "<input>", "single")
        exec(code_obj, self.env)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--db", help="path to the database file", default="pycle.db")
    p.add_argument("-c", "--code", help="code to execute", required=True)
    return p.parse_args()

def main():
    args = parse_args()
    schema.migrate(args.db)
    with Pycle(args.db) as pycle:
        pycle.execute(args.code)