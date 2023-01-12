from Models.truck import Truck
from Models.packages import Packages
from Models.package import Package
from Models.address import Address

from Data.package_data import PackageData
from Data.address_data import AddressData
from Utils.packageSelection import selectPackage

from datetime import timedelta

class Delivery():
    Truck1 = Truck("Driver 1", 1)
    Truck2 = Truck("Driver 2", 2)
    Truck3 = Truck(None, 3)
    unassigned_packages = Packages()
    assigned_packages = Packages()
    delivered_packages = Packages()
    deadlined_packages = Packages()
    


    def __init__(self, package_csv: str, addresses_csv: str) -> None:
        self.unassigned_packages = PackageData.getPackages(package_csv)
        
        addresses = AddressData.getAddresses(addresses_csv)
        self.unassigned_packages.setAddresses(addresses)
        self.assigned_packages.setAddresses(addresses)
        self.delivered_packages.setAddresses(addresses)
        
        self.hubAddress = addresses[0]

        for package in self.unassigned_packages.get_packages():
            deadline = selectPackage.get_deadline(package)
            if deadline:
                self.deadlined_packages.insert_package(package)
        self.deadlined_packages.setAddresses(addresses)


    def loadTruck(self, truck: Truck, departureTime: timedelta):
        route = len(truck.getPackages())+1
        firstPackage = None
        print(len(self.deadlined_packages.get_packages()))
        match len(self.deadlined_packages.get_packages()) > 0:
            case True:
                firstPackage = selectPackage.selectNextShortest(self.deadlined_packages,
                                                                self.hubAddress.Street,
                                                                self.deadlined_packages.addresses,
                                                                truck,
                                                                departureTime)
                if firstPackage[0] != None:
                    selectPackage.addPackage(firstPackage[0],
                                            self.unassigned_packages,
                                            self.assigned_packages,
                                            truck,
                                            departureTime,
                                            firstPackage[1],
                                            route)
                    self.deadlined_packages.delete_package(firstPackage[0].ID)

                    while len(truck._PACKAGES[route -1]) < 16 and len(truck._PACKAGES[route -1]) > 0 and len(self.deadlined_packages.get_packages())>0:
                        nextPackage = selectPackage.selectNextShortest(self.deadlined_packages,
                                                                    self.assigned_packages.select_package(truck._PACKAGES[route-1][-1][0]).ADDRESS,
                                                                    self.deadlined_packages.addresses,
                                                                    truck,
                                                                    departureTime)
                        if nextPackage[0] == None:
                            break

                        selectPackage.addPackage(nextPackage[0],self.unassigned_packages,self.assigned_packages,truck,departureTime,nextPackage[1],route)
                        self.deadlined_packages.delete_package(nextPackage[0].ID)
                else:
                    firstPackage = selectPackage.selectNextShortest(self.unassigned_packages,
                                                                self.hubAddress.Street,
                                                                self.unassigned_packages.addresses,
                                                                truck,
                                                                departureTime)
                    selectPackage.addPackage(firstPackage[0],
                                            self.unassigned_packages,
                                            self.assigned_packages,
                                            truck,
                                            departureTime,
                                            firstPackage[1],
                                            route)
            
            case False:
                firstPackage = selectPackage.selectNextShortest(self.unassigned_packages,
                                                                self.hubAddress.Street,
                                                                self.unassigned_packages.addresses,
                                                                truck,
                                                                departureTime)
                selectPackage.addPackage(firstPackage[0],
                                         self.unassigned_packages,
                                         self.assigned_packages,
                                         truck,
                                         departureTime,
                                         firstPackage[1],
                                         route)
        
        while len(truck._PACKAGES[route-1]) < 16:
            nextPackage = selectPackage.selectNextShortest(self.unassigned_packages,
                                                           self.assigned_packages.select_package(truck._PACKAGES[route-1][-1][0]).ADDRESS,
                                                           self.unassigned_packages.addresses,
                                                           truck,
                                                           departureTime)
            if nextPackage[0] == None:
                break
            selectPackage.addPackage(nextPackage[0],self.unassigned_packages,self.assigned_packages,truck,departureTime,nextPackage[1],route)
        
    def distanceToHub(self, truck: Truck):
        final_package = truck._PACKAGES[-1][-1][0]
        final_address = self.delivered_packages.select_package(final_package).ADDRESS
        address_index = self.delivered_packages.addresses[-1][final_address]
        distance = self.delivered_packages.addresses[address_index].connections[0]
        return distance