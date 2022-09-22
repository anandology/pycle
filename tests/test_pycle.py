from pycle import Pycle
from pycle.schema import migrate
import pytest
import yaml
from pathlib import Path

def read_tests():
    paths = Path(__file__).parent.glob("test_*.yml")
    for p in paths:
        yield from yaml.safe_load_all(p.open())

test_specs = list(read_tests())
test_ids = [test["name"] for test in test_specs]

@pytest.mark.parametrize("spec", test_specs, ids=test_ids)
def test_code(tmp_path, spec):
    db_path = str(tmp_path / "pycle.db")
    migrate(db_path)

    pycle = Pycle(db_path)
    pycle.execute(spec['code'])

    for name, value in spec['env'].items():
        assert pycle.env[name] == value

# def test_strings(db_path):
#     pycle = Pycle(db_path)
#     pycle.execute("name = 'hello'")
#     assert pycle.env['name'] == 'hello'

# def test_functions(db_path):
#     pycle = Pycle(db_path)

#     code = (
#         "def square(x):\n" +
#         "    return x*x\n" +
#         "x = square(5)\n")

#     pycle.execute(code)
#     assert pycle.env['x'] == 25

#     square = pycle.env['square']
#     assert inspect.isfunction(square)
#     assert square(5) == 25