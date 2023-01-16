from Models.package import Package
from Models.packages import Packages
from datetime import datetime, timedelta

from Data.package_data import PackageFields

class Truck():
    """Class to provide a Truck object"""
    def __init__(self,driver,truck_number) -> None:
        """Time Complexity O(1):Space Complexity O(1) Initialize the Truck object with a drive, truck number, 
        and empty packages and distance travelled variables."""
        self._DRIVER =  driver
        self.PACKAGES = []
        self._DISTANCE_TRAVELLED = float()
        self._TRUCK_NUMBER = truck_number
        self.routes = [[]]


    def getPackages(self):
        """Time Complexity O(1):Space Complexity O(1) Gets the PACKAGES variable"""
        return self.PACKAGES

    def getTruckNumber(self):
        """Time Complexity O(1):Space Complexity O(1) Gets the trucks number."""
        return self._TRUCK_NUMBER

    def getAllRoutesLength(self):
        """Time Complexity O(n^2):Space Complexity O(1) Returns the lenght of all the routes added together"""
        distance = 0
        for route in self.routes[1::]: #O(n) loop through the routes in packages
            for package in route: #O(n) loop throught the packages in the route
                distance += package[1] #add the distance of the package to the total distance
        for retdistance in self.routes[0]:# O(n)
            distance += retdistance
        return distance

    def deliverPackages(self, departTime: timedelta, deliveredPackages: Packages, route: int):
        """ Time Complexity O(n^2):Space Complexity O(n) Sets the staus to deliverd and sets the correct delivered time for each package in the route."""
        distanceTraveled = 0 #set route distance traveled to 0
        for stop in self.routes[route]: # O(n) Loop thorugh the route provided.
            distanceTraveled += stop[1] #add the distance at the stop to the distance traveled
            package = stop[0]
            package.STATUS = PackageFields.DELIVERED_STATUS #Set the package Status
            
            timeDelivered = timedelta(hours=distanceTraveled/18) + departTime #calculates the time delivered of the package
            package.TimeDelivered = timeDelivered #Sets the time delivered of the package
            deliveredPackages.insert_package(package) # O(n) Adds the package to the delivered packages HashTable
        self._DISTANCE_TRAVELLED += (distanceTraveled + self.routes[0][route-1]) #add the distanct traveled to the Trucks total distance. 
        return self._DISTANCE_TRAVELLED