import json


class Workspace:
    def __init__(self, workspace):
        self.workspace = workspace
        self.db = None
        self._fetch()

    def set(self, key, value):
        self._fetch()
        self.db[self.workspace][key] = value
        self._update()

    def get(self, key):
        self._fetch()
        return self.db[self.workspace].get(key)

    def _update(self):
        json.dump(self.db, open("./db.json", "w"))

    def _fetch(self):
        print(f"")
        self.db = json.load(open("./db.json", "r"))
        if self.db.get(self.workspace) == None:
            self.db[self.workspace] = {}
            self._update()


# make this update live when other programns edit the file.
