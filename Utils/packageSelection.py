from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck
import Utils.specialNotes as sn


class selectPackage():

    @staticmethod
    def selectNextShortest(unassignedPackages: Packages, currentPackage: Package, addressList: Address) -> Package:
        currentPackageAddress = addressList[addressList[-1][currentPackage.ADDRESS]]
        closest= (None, 10000.00)
        for package in unassignedPackages.get_packages():
            comparePackageAddress = addressList[addressList[-1][package.ADDRESS]]
            if currentPackageAddress.ID > comparePackageAddress.ID:
                distance = currentPackageAddress.connections[comparePackageAddress.ID][1]
                if distance < closest[1]:
                    closest = (package,distance)
                else:
                    continue
            else:
                distance = comparePackageAddress.connections[currentPackageAddress.ID][1]
                if distance < closest[1]:
                    closest = (package,distance)
                else:
                    continue
        return closest[0]

    @staticmethod
    def addPackage(current_package: Package , unassigned_packages: Packages, assigned_packages: Packages, truck: Truck, time):
        packageNote = sn.Actions.translateAction(current_package.NOTES, current_package.ID)
        canAdd, alsoAdd = sn.Actions.verifyAvalible(packageNote,truck,time,unassigned_packages)
        match canAdd:
            case True:
                if len(alsoAdd) == 0:
                    truck.addPackage(current_package.ID,unassigned_packages)
                    assigned_packages.insert_package(current_package)
                else:
                    alsoAdd = list(alsoAdd)
                    truck.addPackage(current_package.ID,unassigned_packages)
                    assigned_packages.insert_package(current_package)
                    current = current_package
                    alsoAdd.remove(current.ID)
                    loop_packages = Packages()
                    for id in alsoAdd:
                        loop_packages.insert_package(unassigned_packages.select_package(id))
                    while len(alsoAdd) > 0:
                        next = selectPackage.selectNextShortest(loop_packages,current,unassigned_packages.addresses)
                        truck.addPackage(next.ID, unassigned_packages)
                        loop_packages.delete_package(next.ID)
                        current = next
                        alsoAdd.remove(next.ID)
                        assigned_packages.insert_package(current)
                return True
            case False:
                print(f"Package {current_package.ID} cannot be added to {truck._TRUCK_NUMBER}")
                return False


    