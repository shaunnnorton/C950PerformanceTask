from enum import Enum as e
from Utils.utils import Utils
from datetime import datetime, timedelta
from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck

class specialActions(e):
    DELAY = 0
    TRUCK = 1
    WITH = 2
    ADDRESS = 3

class Actions():
    @staticmethod
    def verifyAvalible(specialNote: tuple, truck: Truck, currentTime, packages: Packages) -> tuple():
        if len(specialNote) == 0:
            return True, ()
        match specialNote[0]:
            case specialActions.DELAY.value:
                day,opening = Utils.getDefaultDates()
                delayedTime = day.timedelta(hours=specialNote[1],minutes=specialNote[2])
                if delayedTime < currentTime:
                    return True , ()
                else:
                    return False , ()
            case specialActions.TRUCK.value:
                if specialNote[1] != truck.getTruckNumber:
                    return False , ()
                else:
                    return True
            case specialActions.WITH.value:
                for group in packages.grouped_packages:
                    if specialNote[1] in group:
                        if len(group)+len(truck.getPackages())<=16:
                            return True, tuple(group)
                        else:
                            return False, tuple()
            case specialActions.ADDRESS.value:
                day,opening = Utils.getDefaultDates()
                delayedTime = day.timedelta(hours=specialNote[3],minutes=specialNote[4])
                if delayedTime < currentTime:
                    package = packages.select_package(specialNote[1])
                    newAddress = packages.addresses[specialNote[2]]
                    package.ADDRESS = newAddress.Street
                    package.ZIP = newAddress.ZIP
                    return True , ()
                else: 
                    return False , ()
            case _:
                return True, ()


    
    @staticmethod
    def translateAction(note: str, package: int) -> tuple:
        if note == " | ":
            return ()
        split = note.split("|")
        actionString=split[1].strip()
        match actionString[0]:
            case "0":
                return (0,actionString[1:3],actionString[3:5])
            case "1":
                return (1, int(actionString[1::]))
            case "2":
                action = [2,package]
                count=1
                while count+2<=(len(actionString)):
                    action.append(int(actionString[count:count+2]))
                    count+=2
                return tuple(action)
            case "3":
                return (3, package ,actionString[1:3],actionString[3:5],actionString[5:7])
            case _:
                return ()


    @staticmethod
    def groupPackages(packages: Packages):
        for package in packages.get_packages():
            translatedNote = Actions.translateAction(package.NOTES, package.ID)
            if (len(translatedNote)!=0) and (translatedNote[0] == 2):
                if len(packages.grouped_packages) == 0:
                    packages.grouped_packages.append(set(translatedNote[1::]))
                for index, group in enumerate(packages.grouped_packages):
                    if any( ele in group for ele in translatedNote[1::]):
                        packages.grouped_packages[index] = group.union(set(translatedNote[1::]))
                        break
                    else:
                        packages.grouped_packages.append(set(translatedNote[1::]))
            else:
                continue
    