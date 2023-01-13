
class Address():
    """Class to provide data models for Address Objects"""
    def __init__(self,id: int, street: str, zip: str) -> None:
        """Initialize all Class Variables"""
        self.ID = id
        self.Street = street
        self.ZIP = zip
        self.connections = []

    def add_connections(self, connections):
        """Set the connections variable to a new value."""
        self.connections =  connections