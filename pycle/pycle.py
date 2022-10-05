
from calendar import c
# import sqlite3
import argparse
import ast
import io
import sys
import traceback
from .env import FileEnvironment
# from . import schema

class Pycle:
    def __init__(self, env_path):
        self.env = FileEnvironment(env_path)
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def execute(self, code):
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        try:
            head, tail = self._parse_code(code)
            self.do_exec(head)
            self.do_single(tail)
            self.env.save()
        except Exception as e:
            traceback.print_exc()
        finally:
            sys.stdout = stdout
            sys.stderr = stderr

        self.stdout.seek(0)
        self.stderr.seek(0)
        return self.stdout.read(), self.stderr.read()

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

def parse_args():
    p = argparse.ArgumentParser()
    # p.add_argument("--db", help="path to the database file", default="pycle.db")
    p.add_argument("-f", "--env-file", help="path to the env file", default="pycle-env.pkl")
    p.add_argument("-c", "--code", help="code to execute", required=True)
    return p.parse_args()

def main():
    args = parse_args()
    pycle = Pycle(env_path=args.env_file)
    stdout, stderr = pycle.execute(args.code)
    print(stdout, end="")
    print(stderr, end="")