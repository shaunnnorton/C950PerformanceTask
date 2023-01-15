from Models.packages import Packages
from Models.package import Package
from datetime import timedelta

class selectPackage():
    """Class to provide functionality for selecting and adding a package to a truck"""
    @staticmethod
    def selectNextShortest(choice_packages: Packages, currentAddress: int, addressList: dict) -> tuple:
        """O(n^2):O(n) Gets the package with the address closest to the current address from the provided packages list"""
        startAddress = addressList[currentAddress]#Get initial Address Object
        closest= (None, 10000.00) #init the closest variable
        for package in choice_packages.get_packages():# O(n^2) iterate through all provided packages
            comparePackageAddress = addressList[addressList[-1][package.ADDRESS]] #Get the address from the package.
            if startAddress.ID > comparePackageAddress.ID: # IF the start addresses ID is greater than the comparisonID use the start addresses' connections list
                distance = startAddress.connections[comparePackageAddress.ID][1] # get the distance from the connections list
                if distance < closest[1]: #update the closest packge if the distance is closer and the package is avalible
                    closest = (package,distance)
                else:
                    continue
            else: # IF the compare addresses ID is greater than the start address id use the compare addresses' connections list
                distance = comparePackageAddress.connections[startAddress.ID][1]# get the distance from the connections list
                if distance < closest[1]: #update the closest packge if the distance is closer and the package is avalible
                    closest = (package,distance)
                else:
                    continue
        return closest


    @staticmethod
    def get_deadline(package:Package):
        """O(1):O(1) Gets a packages deadline as a timedelta object"""
        deadlineString = package.DEADLINE #Get the deadline string 
        deadline = None
        try: #Try to parse deadline as timedelta. 
            split = deadlineString.strip(" AMP").split(":") #Split string at colin and remove white space and AM/PM
            hours = int(split[0]) #Set hours
            minutes = int(split[1]) #Set minutes
            
            deadline = timedelta(hours=hours, minutes=minutes) #Get deadline
            return deadline
        except: #Could not parse. 
            return None
    