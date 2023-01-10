from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck
import Utils.specialNotes as sn
import Utils.utils as ut
from datetime import datetime,timedelta

class selectPackage():

    @staticmethod
    def selectNextShortest(unassignedPackages: Packages, currentAddress: str, addressList: Address) -> Package:
        startAddress = addressList[addressList[-1][currentAddress]]
        closest= (None, 10000.00)
        for package in unassignedPackages.get_packages():
            comparePackageAddress = addressList[addressList[-1][package.ADDRESS]]
            if startAddress.ID > comparePackageAddress.ID:
                distance = startAddress.connections[comparePackageAddress.ID][1]
                if distance < closest[1]:
                    closest = (package,distance)
                else:
                    continue
            else:
                distance = comparePackageAddress.connections[startAddress.ID][1]
                if distance < closest[1]:
                    closest = (package,distance)
                else:
                    continue
        return closest

    @staticmethod
    def addPackage(current_package: Package , unassigned_packages: Packages, assigned_packages: Packages, truck: Truck, time, distance:int):
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
                    current = current_package
                    alsoAdd.remove(current.ID)
                    loop_packages = Packages()
                    for id in alsoAdd:
                        loop_packages.insert_package(unassigned_packages.select_package(id))
                    while len(alsoAdd) > 0:
                        next = selectPackage.selectNextShortest(loop_packages,current.ADDRESS,unassigned_packages.addresses)
                        truck.addPackage((next[0].ID,next[1]), unassigned_packages)
                        loop_packages.delete_package(next.ID)
                        current = next
                        alsoAdd.remove(next.ID)
                        assigned_packages.insert_package(current)
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
            deadline = datetime.strptime(deadlineString,"%I:%m %p")
            return deadline
        except:
            return None

    