import sqlite3
from pycle.env import Environment
from pycle.schema import migrate
import pytest

@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "pycle.db")
    migrate(path)
    yield path

def test_simple(db_path):
    conn = sqlite3.connect(db_path)
    env = Environment(conn)
    env['x'] = 1
    assert env['x'] == 1