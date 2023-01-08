from enum import Enum as e
from Utils.utils import Utils
from datetime import datetime, timedelta
from Models.packages import Packages
from Models.package import Package
from Models.address import Address

class specialActions(e):
    DELAY = 0
    TRUCK = 1
    WITH = 2
    ADDRESS = 3

class Actions():
    @staticmethod
    def verifyAvalible(specialNote: tuple, truck: Truck, currentTime, packages: Packages) -> tuple(bool,tuple[int]):
        beginDate = datetime.now().date()
        openingTime = datetime(beginDate.year,beginDate.month, beginDate.day, 8, 0, 0, 0)
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
                partneredPackages = list(specialNote[2::])
                truck_packages = truck.getPackages()
                for package in partneredPackages:
                    if package in truck_packages:
                        partneredPackages.delete(package)
                if len(partneredPackages) == 0:
                    return True , ()
                elif len(partneredPackages) + len(truck_packages) <= 16:
                    return True , tuple(partneredPackages)
                else: 
                    return False
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


    
    @staticmethod
    def translateAction(note: str, package: int) -> tuple:
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
                while count<=(len(note)-1):
                    action.append(int(actionString[count:count+2]))
                    count+=2
                return tuple(action)
            case "3":
                return (3, package ,actionString[1:3],actionString[3:5],actionString[5:7])


    