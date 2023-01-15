
class Address():
    """Class to provide data models for Address Objects"""
    def __init__(self,id: int, street: str, zip: str) -> None:
        """O(1):O(1) Initialize all Class Variables"""
        self.ID = id
        self.Street = street
        self.ZIP = zip
        self.connections = []

    def add_connections(self, connections):
        """O(1):O(1) Set the connections variable to a new value."""
        self.connections =  connections