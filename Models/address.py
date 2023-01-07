
class Address():
    ID = None
    Street = None
    City = None
    State = None
    ZIP = None 
    NAME = None
    connections = []
    def __init__(self,id: int, street: str, city: str, state: str, zip: str, name: str) -> None:
        self.ID = id
        self.Street = street
        self.City = city
        self.State = state
        self.ZIP = zip
        self.NAME = name

    def add_connections(self, connections):
        self.connections = connections.sort(key=lambda val: val[1])