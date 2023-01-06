class Address():
    ID = None
    Street = None
    City = None
    State = None
    ZIP = None 
    connections = {}
    def __init__(self,id: int, street: str, city: str, state: str, zip: str) -> None:
        self.ID = id
        self.Street = street
        self.City = city
        self.State = state
        self.ZIP = zip

    def populate_connections(self, connections):
        self.conntections.add(connections)