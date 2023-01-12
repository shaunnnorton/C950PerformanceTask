from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck
import Utils.specialNotes as sn
import Utils.utils as ut
from datetime import datetime,timedelta

class selectPackage():

    @staticmethod
    def selectNextShortest(unassignedPackages: Packages, currentAddress: str, addressList: dict, truck: Truck, time) -> tuple:
        #print(currentAddress , unassignedPackages.get_packages())
        startAddress = addressList[addressList[-1][currentAddress]]
        closest= (None, 10000.00)
        #print(unassignedPackages.get_packages())
        for package in unassignedPackages.get_packages():
            #print(unassignedPackages.get_packages())
            packageNote = sn.Actions.translateAction(package.NOTES,package.ID)
            # try:
            #     avalible, extra = sn.Actions.verifyAvalible(packageNote, truck, time, unassignedPackages)
            # except:
            #     print(packageNote, avalible,  extra)
            avalible, extra = sn.Actions.verifyAvalible(packageNote, truck, time, unassignedPackages)
            comparePackageAddress = addressList[addressList[-1][package.ADDRESS]]
            if startAddress.ID > comparePackageAddress.ID:
                distance = startAddress.connections[comparePackageAddress.ID][1]
                if distance < closest[1] and avalible:
                    closest = (package,distance)
                else:
                    continue
            else:
                distance = comparePackageAddress.connections[startAddress.ID][1]
                if distance < closest[1] and avalible:
                    closest = (package,distance)
                else:
                    continue
        return closest

    @staticmethod
    def addPackage(current_package: Package , unassigned_packages: Packages, assigned_packages: Packages, truck: Truck, time, distance:int):
        print(current_package.ID)
        packageNote = sn.Actions.translateAction(current_package.NOTES, current_package.ID)
        canAdd, alsoAdd = sn.Actions.verifyAvalible(packageNote,truck,time,unassigned_packages)
        match canAdd:
            case True:
                if len(alsoAdd) == 0:
                    truck.addPackage((current_package.ID,distance),unassigned_packages)
                    assigned_packages.insert_package(current_package)
                else:
                    alsoAdd = list(alsoAdd)
                    truck.addPackage((current_package.ID,distance),unassigned_packages)
                    assigned_packages.insert_package(current_package)
                    current = (current_package,0)
                    alsoAdd.remove(current[0].ID)
                    loop_packages = Packages()
                    print(alsoAdd)
                    for id in alsoAdd:
                        print(id)
                        loop_packages.insert_package(unassigned_packages.select_package(id))
                    while len(alsoAdd) > 0:
                        next = selectPackage.selectNextShortest(loop_packages,current[0].ADDRESS,unassigned_packages.addresses,truck,time)
                        truck.addPackage((next[0].ID,next[1]), unassigned_packages)
                        loop_packages.delete_package(next[0].ID)
                        current = next
                        alsoAdd.remove(next[0].ID)
                        assigned_packages.insert_package(current[0])
                return True
            case False:
                print(f"Package {current_package.ID} cannot be added to {truck._TRUCK_NUMBER}")
                return False

    @staticmethod
    def get_deadline(package:Package):
        day, opening = ut.Utils.getDefaultDates()
        deadlineString = package.DEADLINE
        deadline = None
        try:
            deadline = datetime.strptime(deadlineString,"%H:%M %p")
            return deadline
        except:
            
            return None
        # deadline = datetime.strptime(deadlineString,"%H:%M %p")
        # return deadline
    