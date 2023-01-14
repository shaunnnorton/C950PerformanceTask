from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck
import Utils.specialNotes as sn
import Utils.utils as ut
from datetime import datetime,timedelta

class selectPackage():
    """Class to provide functionality for selecting and adding a package to a truck"""
    @staticmethod
    def selectNextShortest(unassignedPackages: Packages, currentAddress: str, addressList: dict) -> tuple:
        startAddress = addressList[addressList[-1][currentAddress]]#Get initial Address Object
        closest= (None, 10000.00) #init the closest variable
        for package in unassignedPackages.get_packages():#iterate through all provided packages
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

    # DEPRECIATED
    # @staticmethod
    # def addPackage(current_package: Package , unassigned_packages: Packages, assigned_packages: Packages, truck: Truck, time:timedelta, distance:int, route: int):
    #     """Adds the package to the passed truck if it can be added."""
    #     packageNote = sn.Actions.translateAction(current_package.NOTES, current_package.ID) #Translates the packages notes
    #     canAdd, alsoAdd = sn.Actions.verifyAvalible(packageNote,truck,time,unassigned_packages) #Verifies the package can be added. 
    #     match canAdd:
    #         case True: #If the package can be added
    #             if len(alsoAdd) == 0: #IF the package does not need to be added with other packages.
    #                 truck.addPackage((current_package.ID,distance),unassigned_packages, route) #add the packge to the truck 
    #                 assigned_packages.insert_package(current_package) #add the package to the assigned packages hash table
    #                 current_package.TransitTime = time #Set the packages transit time
    #             else: #If the package must be added with others. 
    #                 alsoAdd = list(alsoAdd) #get the other packges as a list
    #                 truck.addPackage((current_package.ID,distance),unassigned_packages, route)# add the current packge to the turck
    #                 assigned_packages.insert_package(current_package) #add the package to the assigned packages hash table
    #                 current_package.TransitTime = time #Set the packages transit time
    #                 current = (current_package,0) # Set the current varibale
    #                 alsoAdd.remove(current[0].ID) # remove the package id from the also add list
    #                 loop_packages = Packages() # create the packges we will loop thorugh
    #                 for id in alsoAdd: # populate loop packages with the packages from also add
    #                     loop_packages.insert_package(unassigned_packages.select_package(id))
    #                 while len(alsoAdd) > 0: #While there are still packges to add
    #                     next = selectPackage.selectNextShortest(loop_packages,current[0].ADDRESS,unassigned_packages.addresses,truck,time) #get the next closet packge from the loop packges
    #                     truck.addPackage((next[0].ID,next[1]), unassigned_packages, route)# add the next packge to the truck
    #                     loop_packages.delete_package(next[0].ID) #remove the next packge from loop_packages hash table
    #                     next[0].TransitTime = time #set the packges transit time. 
    #                     current = next # Iterate current to the next package
    #                     alsoAdd.remove(next[0].ID) #Remove the next packages id from also add
    #                     assigned_packages.insert_package(current[0]) #add the packge to assigned packages. 
    #             return True
    #         case False: #Print an message and return false if package can not be added. 
    #             print(f"Package {current_package.ID} cannot be added to {truck._TRUCK_NUMBER}")
    #             return False

    @staticmethod
    def get_deadline(package:Package):
        """Gets a packages deadline as a datetime object"""
        deadlineString = package.DEADLINE #Get the deadline string 
        deadline = None
        try: #Try to parse deadline as datetime. 
            deadline = datetime.strptime(deadlineString,"%H:%M %p")
            return deadline
        except: #Could not parse. 
            
            return None
    