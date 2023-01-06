
class Package():
    ID = None
    ADDRESS = None
    DEADLINE = None
    CITY = None
    STATE = None
    ZIP = None
    STATUS = None
    def __init__(self,id: int,address: str,deadline: str,city: str,state: str,zip: str ,status: int) -> None:
        self.ID = id
        self.ADDRESS = address
        self.DEADLINE = deadline
        self.CITY = city
        self.STATE = state
        self.ZIP = zip
        self.STATUS = status

    def toList(self):
        return [self.ID, self.ADDRESS, self.DEADLINE, self.CITY, self.STATE, self.ZIP, self.STATUS]