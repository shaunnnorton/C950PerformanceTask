from enum import Enum as e
from datetime import timedelta
from Models.packages import Packages
from Models.truck import Truck

class specialActions(e):
    """Enum to provide a standard explination for special actions in the notes"""
    DELAY = 0
    TRUCK = 1
    WITH = 2
    ADDRESS = 3

class Actions():
    """Provides a class for actions that can be taken from the notes on a package"""
    @staticmethod
    def verifyAvalible(specialNote: tuple, truck: Truck, currentTime: timedelta, packages: Packages) -> tuple:
        """O(n):O(n) Checks if the conditions of a packages special notes are met and returns a tuple of additionl packages to add."""
        if len(specialNote) == 0:#If the special note contains no elements default to true with no addtional packages
            return True, ()
        match specialNote[0]:#match the first value of the special note to a special action. 
            case specialActions.DELAY.value: #Action to delay package. 
                delayedTime = timedelta(hours=specialNote[1],minutes=specialNote[2]) #get the time to delay to
                if delayedTime <= currentTime: #Check if the current time is past the delayed time
                    return True , () 
                else:
                    return False , ()
            case specialActions.TRUCK.value: #Action to specify a truck for the package
                if specialNote[1] != truck.getTruckNumber(): #check if the truck number matches that in the special note
                    return False , ()
                else:
                    return True , ()
            case specialActions.WITH.value: #Action to specify packages to be delivered with this package
                for group in packages.grouped_packages: #O(n) loop the grouped packages set in the packages hash table 
                    if specialNote[1] in group: #check if the currnent package is in a group
                        if len(group)+len(truck.getPackages()[-1])<=16: #Check if there is room in the truck for all the grouped packages.
                            packages.grouped_packages.remove(group)
                            return True, tuple(group)
                        else: #return false if there is not room for the package. 
                            return False, ()
                return True, () #return True if the package is not in a group. 
            case specialActions.ADDRESS.value: #Action to specify a delay with address change. 
                delayedTime = timedelta(hours=specialNote[3],minutes=specialNote[4]) #Set the time to delay the packge delivery to
                if delayedTime < currentTime: #Check it is past the time to delay
                    package = packages.select_package(specialNote[1]) #O(n) Get the package object matching this ID
                    newAddress = packages.addresses[specialNote[2]] #Get the packages new address
                    package.ADDRESS = newAddress.Street #set the packages new address
                    package.ZIP = newAddress.ZIP #set the packages new Zip
                    return True , ()
                else: #return false if the time is too soon. 
                    return False , ()
            case _: #Return True as a default if no case matches
                return True, ()


    
    @staticmethod
    def translateAction(note: str, package: int) -> tuple:
        """ O(n):O(n) Translates a note from a package into a meaningfull tuple"""
        if note == " | ": #If the note matches the default case return a default tuple.
            return (-1,package)
        split = note.split("|") #Split the note at the bar to gather the second part of the string.
        actionString=split[1].strip() #Strip the string of whitespaces
        match actionString[0]: #Match the first character of the string with a case
            case "0": # Delayed case
                # Returns format (0, hours, minutes)
                return (0,int(actionString[1:3]),int(actionString[3:5]))
            case "1": # On Truck case
                # Returns format (0, trucknumber)
                return (1, int(actionString[1::]))
            case "2": # Grouped Case
                # Returns format (2, packageID, Id1, Id2, ...)
                action = [2,package]
                count=1
                while count+2<=(len(actionString)): #O(n) add all two digit ids to the return
                    action.append(int(actionString[count:count+2]))
                    count+=2
                return tuple(action)
            case "3": # Address Case
                # Returns format (3, packageID, newAddressID, delayedHour, delayedMinute)
                return (3, package ,int(actionString[1:3]),int(actionString[3:5]),int(actionString[5:7]))
            case _: #Default Case
                return (-1,package)


    @staticmethod
    def groupPackages(packages: Packages):
        """O(n^3): O(n^3) Populates the grouped packages of the packages hash table"""
        for package in packages.get_packages():# O(n^2)Iterate through each package
            translatedNote = Actions.translateAction(package.NOTES, package.ID) # O(n)Translate the note on the package
            if (len(translatedNote)!=0) and (translatedNote[0] == 2): #check the note length > 0 and that it is a grouped package.
                if len(packages.grouped_packages) == 0: #Create a new set if the grouped packages is empty
                    packages.grouped_packages.append(set(translatedNote[1::]))
                for index, group in enumerate(packages.grouped_packages): # O(n) loop thorugh the grouped packages of the hash table
                    if any( ele in group for ele in translatedNote[1::]): #If any of the grouped packages are in the set joint the two sets together. 
                        packages.grouped_packages[index] = group.union(set(translatedNote[1::]))
                        break
                    else:
                        packages.grouped_packages.append(set(translatedNote[1::])) #Create a new set of gropued packages
            else:
                continue
    