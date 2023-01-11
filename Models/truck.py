from Models.package import Package
from Models.packages import Packages
from datetime import datetime, timedelta
class Truck():
    def __init__(self,driver,truck_number) -> None:
        self._DRIVER =  driver
        self._PACKAGES = []
        self._DISTANCE_TRAVELLED = 0
        self._TRUCK_NUMBER = truck_number

    def setDriver(self, name:str):
        self._DRIVER = name
    
    def getDriver(self):
        return self._DRIVER

    def addPackage(self, package: tuple, packageList: Packages):
        self._PACKAGES.append(package)
        packageList.delete_package(package[0])
    
    def getPackages(self):
        return self._PACKAGES

    def removePackage(self, package: Package):
        self._PACKAGES.remove(package)

    def setTruckNumber(self, num: int):
        self._TRUCK_NUMBER = num

    def getTruckNumber(self):
        return self._TRUCK_NUMBER

    def getRouteLength(self):
        distance = 0
        for i in self._PACKAGES:
            distance += i[1]
        return distance

    def traveledAtTime(self,time: datetime):
        totalRouteTime = self.getRouteLength()+self._DISTANCE_TRAVELLED/18
        timeSinceOpen = time - timedelta(hours=8)
