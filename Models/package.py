from Data.package_data import PackageFields
from datetime import timedelta

class Package():
    """Class to provide a data model for a Package"""
    def __init__(self,id: int,address: str,deadline: str,city: str,state: str,zip: str ,status: PackageFields, weight: float, notes: str) -> None:
        """Initialize Package with all variables"""
        self.ID = id
        self.ADDRESS = address
        self.DEADLINE = deadline
        self.CITY = city
        self.STATE = state
        self.ZIP = zip
        self.STATUS = status
        self.WEIGHT = weight
        self.NOTES = notes
        self.TimeDelivered = timedelta()
        self.TransitTime = timedelta()

    def toTuple(self):
        """Returns a tuple containg all the Package information."""
        return (self.ID, self.ADDRESS, self.DEADLINE, self.CITY, self.STATE, self.ZIP, self.STATUS)