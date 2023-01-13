from Models.truck import Truck
from Models.packages import Packages
from Models.package import Package
from Models.address import Address

from Data.package_data import PackageData, PackageFields
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
    


    def __init__(self, package_csv: str, addresses_csv: str, initialTime: timedelta) -> None:
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

        self.initial_time = initialTime


    def loadTruck(self, truck: Truck, departureTime: timedelta):
        route = len(truck.getPackages())+1
        firstPackage = None
        #print(len(self.deadlined_packages.get_packages()))
        match len(self.deadlined_packages.get_packages()) > 0:
            case True:
                print(departureTime)
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
                    if firstPackage[0] != None:
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
                if firstPackage[0] != None:
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
        
    def distanceToHub(self, truck: Truck, route: int) -> float:
        final_package = truck._PACKAGES[route-1][-1][0]
        final_address = self.assigned_packages.select_package(final_package).ADDRESS
        address_index = self.assigned_packages.addresses[-1][final_address]
        distance = self.assigned_packages.addresses[address_index].connections[0]
        return distance[1]

    def createRoutes(self) -> None:
        self.loadTruck(self.Truck1, self.initial_time)
        self.loadTruck(self.Truck2, self.initial_time)
        truck1_return_distance = self.distanceToHub(self.Truck1,1)
        truck2_return_distance = self.distanceToHub(self.Truck2,1)
        while len(self.unassigned_packages.get_packages()) > 0:
            truck1_total = self.Truck1.getAllRoutesLength() + truck1_return_distance
            truck2_total = self.Truck2.getAllRoutesLength() + truck2_return_distance
            if truck1_total < truck2_total:
                self.loadTruck(self.Truck1, timedelta(hours=truck1_total/18) + self.initial_time)
            else:
                self.loadTruck(self.Truck2, timedelta(hours=truck1_total/18) + self.initial_time)

    def deliverAll(self):
        depart_Time = self.initial_time
        for index, route in enumerate(self.Truck1._PACKAGES):
            depart_Time = self.assigned_packages.select_package(self.Truck1._PACKAGES[index][-1][0]).TransitTime
            self.Truck1.deliverPackages(depart_Time,self.assigned_packages,self.delivered_packages,index+1)
            self.Truck1._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck1,index+1)
       
        depart_Time = self.initial_time
        for index, route in enumerate(self.Truck2._PACKAGES):
            depart_Time = self.assigned_packages.select_package(self.Truck2._PACKAGES[index][-1][0]).TransitTime
            self.Truck2.deliverPackages(depart_Time,self.assigned_packages,self.delivered_packages,index+1)
            self.Truck2._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck2,index+1)
            
            print("TRUCK@", depart_Time)

    def getPackageStatus(self, id: int, time: timedelta):
        package = self.delivered_packages.select_package(id)
        transit = package.TransitTime
        delivered = package.TimeDelivered
        #print(package.ID, transit, delivered, time)
        if time < transit:
            return PackageFields.HUB_STATUS
        elif time > transit and time < delivered:
            return PackageFields.TRANSIT_STATUS
        else:
            return PackageFields.DELIVERED_STATUS

    def getAllPackageStatus(self, time) -> dict:
        statuses = {
            PackageFields.HUB_STATUS:[],
            PackageFields.DELIVERED_STATUS:[],
            PackageFields.TRANSIT_STATUS:[]
        }
        for package in self.assigned_packages.get_packages():
            status = self.getPackageStatus(package.ID, time)
            statuses[status].append(package)
        return statuses