from Models.package import Package
from Models.packages import Packages
from datetime import datetime, timedelta

from Data.package_data import PackageFields

class Truck():
    """Class to provide a Truck object"""
    def __init__(self,driver,truck_number) -> None:
        """Initialize the Truck object with a drive, truck number, 
        and empty packages and distance travelled variables."""
        self._DRIVER =  driver
        self._PACKAGES = []
        self._DISTANCE_TRAVELLED = float()
        self._TRUCK_NUMBER = truck_number

    def setDriver(self, name:str):
        """Set the driver field of the Truck"""
        self._DRIVER = name
    
    def getDriver(self):
        """Gets the driver field of the Truck"""
        return self._DRIVER

    def addPackage(self, package: tuple, packageList: Packages, route:int):
        """Adds a package to the truck in the proper route"""
        if len(self._PACKAGES) < route:#Creates a new list to serve as a route if the route does not exist
            self._PACKAGES.append([])        
        self._PACKAGES[route-1].append(package) #Add the package to the route
        packageList.select_package(package[0]).STATUS = PackageFields.TRANSIT_STATUS #changes the package status to Transit. 
        packageList.delete_package(package[0]) #removes the package from the package list provided
    
    def getPackages(self):
        """Gets the _PACKAGES variable"""
        return self._PACKAGES


    def setTruckNumber(self, num: int):
        """Sets the Truck Number"""
        self._TRUCK_NUMBER = num

    def getTruckNumber(self):
        """Gets the trucks number."""
        return self._TRUCK_NUMBER

    def getAllRoutesLength(self):
        """Returns the lenght of all the routes added together"""
        distance = 0
        for route in self._PACKAGES:#loop through the routes in packages
            for package in route: #loop throught the packages in the route
                distance += package[1] #add the distance of the package to the total distance
        return distance

    def deliverPackages(self, departTime: timedelta, packagesHash: Packages, deliveredPackages: Packages, route: int):
        """Sets the staus to deliverd and sets the correct delivered time for each package in the route."""
        distanceTraveled = 0 #set route distance traveled to 0
        for stop in self._PACKAGES[route-1]: #Loop thorugh the route provided.
            distanceTraveled += stop[1] #add the distance at the stop to the distance traveled

            package = packagesHash.select_package(stop[0]) #Get the package object at the stop
            package.STATUS = PackageFields.DELIVERED_STATUS #Set the package Status
            
            timeDelivered = timedelta(hours=distanceTraveled/18) + departTime #calculates the time delivered of the package
            package.TimeDelivered = timeDelivered #Sets the time delivered of the package
            deliveredPackages.insert_package(package) #Adds the package to the delivered packages HashTable
        self._DISTANCE_TRAVELLED += distanceTraveled #add the distanct traveled to the Trucks total distance. 
        return self._DISTANCE_TRAVELLED