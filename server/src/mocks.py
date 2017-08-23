class OneResult:
    def __init__(self, result = None):
        self.result = result
    def one(self):
        return self.result

class ShallowFilter:
    def __init__(self, anything = None):
        self.dataToReturn = anything
    def filter(self, any):
        return OneResult(self.dataToReturn)
    def filter_by(self, **any):
        return [self.dataToReturn]

class MockFilterProvider:
    def __init__(self, data = None):
        self.data = data
    def query(self, any):
        return ShallowFilter(self.data)

class MockUser:
    def __init__(self, username = None, password = None, name = None, score = None, team = None):
        self.username = username
        self.password = password
        self.team_name = team
        self.score = score
        self.name = name

class MockTeam:
    def __init__(self, name = None, users = None):
        self.name = name
        self.members = users

class MockAdderDatabase:
    def add(self, user):
        if user.username == "fail":
            raise Exception("db simulated failure")
        return
    def query(self, filter):
        return ShallowFilter(MockUser("anything"))
    def rollback(self):
        return
    def commit(self):
        return

class FaultyCommitDatabase:
    def query(self, filter):
        return ShallowFilter(MockUser("anything"))
    def rollback(self):
        return
    def commit(self):
        raise Exception("db simulated failure")