
class Address():
    ID = None
    Street = None
    ZIP = None 
    connections = []
    def __init__(self,id: int, street: str, zip: str) -> None:
        self.ID = id
        self.Street = street
        self.ZIP = zip

    def add_connections(self, connections):
        self.connections = connections.sort(key=lambda val: val[1])