from Models.package import Package
class Truck():
    _DRIVER = ''
    _PACKAGES = {}
    #_DISTANCE_TRAVELLED = 0
    _TRUCK_NUMBER = 0

    def setDriver(self, name:str):
        self._DRIVER = name
    
    def getDriver(self):
        return self._DRIVER

    def addPackage(self, package: int):
        self._PACKAGES.add(package)
    
    def getPackages(self):
        return self._PACKAGES

    def removePackage(self, package: Package):
        self._PACKAGES.remove(package)

    def setTruckNumber(self, num: int):
        self._TRUCK_NUMBER = num

    def getTruckNumber(self):
        return self._TRUCK_NUMBER
    