from Models.package import Package
from Models.packages import Packages
from datetime import datetime, timedelta

from Data.package_data import PackageFields

class Truck():
    def __init__(self,driver,truck_number) -> None:
        self._DRIVER =  driver
        self._PACKAGES = []
        self._DISTANCE_TRAVELLED = float()
        self._TRUCK_NUMBER = truck_number

    def setDriver(self, name:str):
        self._DRIVER = name
    
    def getDriver(self):
        return self._DRIVER

    def addPackage(self, package: tuple, packageList: Packages, route:int):
        if len(self._PACKAGES) < route:
            self._PACKAGES.append([])        
        self._PACKAGES[route-1].append(package)
        packageList.select_package(package[0]).STATUS = PackageFields.TRANSIT_STATUS
        packageList.delete_package(package[0])
    
    def getPackages(self):
        return self._PACKAGES

    def removePackage(self, package: Package):
        self._PACKAGES.remove(package)

    def setTruckNumber(self, num: int):
        self._TRUCK_NUMBER = num

    def getTruckNumber(self):
        return self._TRUCK_NUMBER

    def getAllRoutesLength(self):
        distance = 0
        for i in self._PACKAGES:
            for j in i:
                distance += j[1]
        return distance

    # def traveledAtTime(self,time: datetime):
    #     totalRouteTime = self.getRouteLength()+self._DISTANCE_TRAVELLED/18
    #     timeSinceOpen = time - timedelta(hours=8)
    
    def deliverPackages(self, departTime: timedelta, packagesHash: Packages, deliveredPackages: Packages, route: int):
        distanceTraveled = 0
        for stop in self._PACKAGES[route-1]:
            distanceTraveled += stop[1]

            package = packagesHash.select_package(stop[0])
            package.STATUS = PackageFields.DELIVERED_STATUS
            
            timeDelivered = timedelta(hours=distanceTraveled/18) + departTime
            package.TimeDelivered = timeDelivered
            deliveredPackages.insert_package(package)
        self._DISTANCE_TRAVELLED += distanceTraveled
        return self._DISTANCE_TRAVELLED