from Models.packages import Packages
from Models.package import Package
from Models.address import Address
from Models.truck import Truck


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




    