from Models.package import Package
from Models.packages import Packages
class Truck():
    _DRIVER = ''
    _PACKAGES = []
    #_DISTANCE_TRAVELLED = 0
    _TRUCK_NUMBER = 0

    def setDriver(self, name:str):
        self._DRIVER = name
    
    def getDriver(self):
        return self._DRIVER

    def addPackage(self, package: int, packageList: Packages):
        self._PACKAGES.append(package)
        packageList.delete_package(package)
    
    def getPackages(self):
        return self._PACKAGES

    def removePackage(self, package: Package):
        self._PACKAGES.remove(package)

    def setTruckNumber(self, num: int):
        self._TRUCK_NUMBER = num

    def getTruckNumber(self):
        return self._TRUCK_NUMBER
    