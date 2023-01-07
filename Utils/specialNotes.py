from enum import Enum as e

class specialActions(e):
    DELAY = 0
    TRUCK = 1
    WITH = 2
    ADDRESS = 3

class Actions():
    @staticmethod
    def verifyAvalible(specialNote: tuple, truck: Truck, currentTime) -> bool:
        match specialNote[0]:
            case specialActions.DELAY:
                pass
            case specialActions.TRUCK:
                if specialNote[1] != truck.getTruckNumber:
                    return False
                else:
                    return True
            case specialActions.WITH:
                remainingPackages = list(specialNote[2::])
                truck_packages = truck.getPackages()
                for package in remainingPackages:
                    if package in truck_packages:
                        remainingPackages.delete(package)
                if remainingPackages == 0:
                    return True
                elif len(remainingPackages) + len(truck_packages) <= 16:
                    for i in remainingPackages:
                        truck.addPackage(i)
                    return True
                else: 
                    return False
            case specialActions.ADDRESS:
                pass


    
    @staticmethod
    def translateAction(note: str, package: int) -> tuple:
        split = note.split("|")
        actionString=split[1].strip()
        match actionString[0]:
            case "0":
                return (0, actionString[1:3],actionString[3:5])
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
                return (3, actionString[1:3],actionString[3:5],actionString[5:7])
