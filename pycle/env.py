import cloudpickle
from pathlib import Path

class FileEnvironment(dict):
    """Environment that is saved as a single file.
    """
    def __init__(self, path):
        self.path = Path(path)
        self.update(self._load(self.path))

    def _load(self, path: Path) -> dict:
        """Load the env from a file.
        """
        if not self.path.exists():
            return {}

        with self.path.open("rb") as f:
            return cloudpickle.load(f)

    def save(self):
        pickled_value = cloudpickle.dumps(dict(self))
        with self.path.open("wb") as f:
            cloudpickle.dump(self, f)

class SqliteEnvironment(dict):
    """Environment that saves the env in a sqlite db.

    Not: The initial plan was to save every variable seperately, but had
    to pickle the entire env as a single entry to retains the references
    correctly.

    This is not used anymore and the FileEnvironment is used now.
    """
    def __init__(self, conn):
        self.conn = conn

        try:
            self.update(self._load("_env"))
        except KeyError:
            pass

    def query(self, q, params=[]):
        # print("QUERY:", q, params)
        cursor = self.conn.cursor()
        cursor.execute(q, params)
        return cursor.fetchall()

    def _delete(self, name):
        self.query("DELETE FROM env WHERE name=?", [name])

    def _insert(self, name, value):
        self.query("INSERT INTO env (name, value) VALUES (?, ?)", [name, value])
        self.conn.commit()

    def _load(self, name):
        result = self.query("SELECT value FROM env where name=?", [name])
        if not result:
            raise KeyError(name)
        pickled_value = result[0][0]
        return cloudpickle.loads(pickled_value)

    def save(self):
        pickled_value = cloudpickle.dumps(dict(self))
        self._delete("_env")
        self._insert("_env", pickled_value)

    # def __getitem__(self, name):
    #     if name not in self:
    #         super().__setitem__(name, self._load(name))
    #     return super().__getitem__(name)

    # def __setitem__(self, name, value):
    #     super().__setitem__(name, value)

    #     pickled_value = cloudpickle.dumps(value)
    #     self._delete(name)
    #     self._insert(name, pickled_value)


