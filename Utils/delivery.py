from Models.truck import Truck
from Models.packages import Packages
from Models.package import Package
from Models.address import Address

from Data.package_data import PackageData, PackageFields
from Data.address_data import AddressData
from Utils.packageSelection import selectPackage
from Utils.specialNotes import Actions

from datetime import timedelta

class Delivery():
    """Class to provide Delivery Management"""
    Truck1 = Truck("Driver 1", 1)
    Truck2 = Truck("Driver 2", 2)
    Truck3 = Truck(None, 3)
    unassigned_packages = Packages()
    assigned_packages = Packages()
    delivered_packages = Packages()
    deadlined_packages = Packages()
    


    def __init__(self, package_csv: str, addresses_csv: str, initialTime: timedelta) -> None:
        """INIT all variables and populate packages and addressses"""
        self.unassigned_packages = PackageData.getPackages(package_csv)
        
        addresses = AddressData.getAddresses(addresses_csv)
        self.unassigned_packages.setAddresses(addresses)
        self.assigned_packages.setAddresses(addresses)
        self.delivered_packages.setAddresses(addresses)
        
        Actions.groupPackages(self.unassigned_packages)

        self.hubAddress = addresses[0]

        for package in self.unassigned_packages.get_packages():#Add all packages with a deadline to deadlined packages
            deadline = selectPackage.get_deadline(package)
            if deadline:
                self.deadlined_packages.insert_package(package)
        self.deadlined_packages.setAddresses(addresses)

        self.initial_time = initialTime


    def loadTruck(self, truck: Truck, departureTime: timedelta):
        """Loads packages starting with deadlined packages into a truck"""
        route = len(truck.getPackages())+1 #Get the new route number. 
        truck._PACKAGES.append([])
        firstPackage = None
        match len(self.deadlined_packages.get_packages()) > 0: #Check if there are still deadlined packages to adds
            case True:#add deadlined packges
                firstPackage = selectPackage.selectNextShortest(self.deadlined_packages, #set the first packge to the deadlined packge closest to the hub. 
                                                                self.hubAddress.Street,
                                                                self.deadlined_packages.addresses,
                                                                truck,
                                                                departureTime)
                if firstPackage[0] != None: # If there is a deadlined package avalible continue
                    selectPackage.addPackage(firstPackage[0], #add the fisrt package to the truck 
                                            self.unassigned_packages,
                                            self.assigned_packages,
                                            truck,
                                            departureTime,
                                            firstPackage[1],
                                            route)
                    self.deadlined_packages.delete_package(firstPackage[0].ID) #remove the deadline from deadlined_packages

                    while len(truck._PACKAGES[route -1]) < 16 and len(truck._PACKAGES[route -1]) > 0 and len(self.deadlined_packages.get_packages())>0: #add all deadlined packages
                        nextPackage = selectPackage.selectNextShortest(self.deadlined_packages, #get the next shortest package
                                                                    self.assigned_packages.select_package(truck._PACKAGES[route-1][-1][0]).ADDRESS,
                                                                    self.deadlined_packages.addresses,
                                                                    truck,
                                                                    departureTime)
                        
                        

                        if nextPackage[0] == None: #If there is no next package I.e all not avalible or empty set break. 
                            break

                        if self.unassigned_packages.select_package(nextPackage[0].ID) == None:
                            self.deadlined_packages.delete_package(nextPackage[0].ID)
                            continue

                        selectPackage.addPackage(nextPackage[0],self.unassigned_packages,self.assigned_packages,truck,departureTime,nextPackage[1],route)# add the next packge to the truck
                        self.deadlined_packages.delete_package(nextPackage[0].ID) # remove the package from the deadlined packges. 
                else: 
                    firstPackage = selectPackage.selectNextShortest(self.unassigned_packages, #select a next packge from all
                                                                self.hubAddress.Street,
                                                                self.unassigned_packages.addresses,
                                                                truck,
                                                                departureTime)
                    if firstPackage[0] != None: #continue if a package is selected
                        selectPackage.addPackage(firstPackage[0], #add the package to the truck
                                                self.unassigned_packages,
                                                self.assigned_packages,
                                                truck,
                                                departureTime,
                                                firstPackage[1],
                                                route)
            
            case False:
                firstPackage = selectPackage.selectNextShortest(self.unassigned_packages, #set the first package from all packages
                                                                self.hubAddress.Street,
                                                                self.unassigned_packages.addresses,
                                                                truck,
                                                                departureTime)
                if firstPackage[0] != None:
                    selectPackage.addPackage(firstPackage[0], #add the first package to the truck
                                            self.unassigned_packages,
                                            self.assigned_packages,
                                            truck,
                                            departureTime,
                                            firstPackage[1],
                                            route)
        if(firstPackage[0] != None):
            while len(truck._PACKAGES[route-1]) < 16: #Add packages until the trucks lenght is 16 or non are avalible. After avalible deadlined packages are exuasted.
                nextPackage = selectPackage.selectNextShortest(self.unassigned_packages, #Select the next package
                                                            self.assigned_packages.select_package(truck._PACKAGES[route-1][-1][0]).ADDRESS,
                                                            self.unassigned_packages.addresses,
                                                            truck,
                                                            departureTime)
                if nextPackage[0] == None:
                    break
                selectPackage.addPackage(nextPackage[0],self.unassigned_packages,self.assigned_packages,truck,departureTime,nextPackage[1],route) #add the packge to the truck
        
    def distanceToHub(self, truck: Truck, route: int) -> float:
        """Calculate a trucks distance to the hub at the end of a route"""
        final_package = truck._PACKAGES[route-1][-1][0] #Get the final package of the route
        final_address = self.assigned_packages.select_package(final_package).ADDRESS #get the final packages addresss
        address_index = self.assigned_packages.addresses[-1][final_address] # get the index of the final address. 
        distance = self.assigned_packages.addresses[address_index].connections[0] # get the distance to the hub
        return distance[1] # return the distance. 

    def createRoutes(self) -> None:
        """Creates all rotues needed to deliver all packages in 2 Trucks."""
        self.loadTruck(self.Truck1, timedelta(hours=9,minutes=5)) #Load the trucks first route using the inital time
        self.loadTruck(self.Truck2, self.initial_time) #Load the trucks first route using the inital time
        truck1_return_distance = self.distanceToHub(self.Truck1,1) #get distance needed for the truck to return to the warehouse
        truck2_return_distance = self.distanceToHub(self.Truck2,1) #get distance needed for the truck to return to the warehouse
        while len(self.unassigned_packages.get_packages()) > 0: #While there are still packages to add. 
            truck1_total = self.Truck1.getAllRoutesLength() + truck1_return_distance #Calculate the total length of the route and distacne to come back 
            truck2_total = self.Truck2.getAllRoutesLength() + truck2_return_distance #Calculate the total length of the route and distacne to come back
            if truck1_total < truck2_total: #Use the truck that comes back first I.E. Has the shortest total
                self.loadTruck(self.Truck1, timedelta(hours=truck1_total/18) + timedelta(hours=9,minutes=5)) #load truck again, with new departure time. 
            else:
                self.loadTruck(self.Truck2, timedelta(hours=truck1_total/18) + self.initial_time) #load truck again, with new departure time. 

    def deliverAll(self):
        """Sets packages in every truck to delivered and populates their delivered time."""
        for index, route in enumerate(self.Truck1._PACKAGES):
            depart_Time = self.assigned_packages.select_package(self.Truck1._PACKAGES[index][-1][0]).TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck1.deliverPackages(depart_Time,self.assigned_packages,self.delivered_packages,index+1) #Deliver the packges in the truck
            self.Truck1._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck1,index+1) #add the distance to hub to the total distanct traveled
            

        for index, route in enumerate(self.Truck2._PACKAGES):
            depart_Time = self.assigned_packages.select_package(self.Truck2._PACKAGES[index][-1][0]).TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck2.deliverPackages(depart_Time,self.assigned_packages,self.delivered_packages,index+1) #Deliver the packges in the truck
            self.Truck2._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck2,index+1) #add the distance to hub to the total distanct traveled

    def getPackageStatus(self, id: int, time: timedelta) -> PackageFields:
        """Get the status of a package at a specific time"""
        package = self.delivered_packages.select_package(id) #Get the package
        transit = package.TransitTime #Get the packages transit time
        delivered = package.TimeDelivered #get the packages time deliverd
        if time < transit: #If time is before the time it is in transit it is at the hub
            return PackageFields.HUB_STATUS
        elif time >= transit and time < delivered: #If the time is between transit and deliverd it is in transit
            return PackageFields.TRANSIT_STATUS
        else: #Otherwise the package is in a delivered status
            return PackageFields.DELIVERED_STATUS

    def getAllPackageStatus(self, time) -> dict:
        """Gets all the packages statuses at a time"""
        statuses = {
            PackageFields.HUB_STATUS:[],
            PackageFields.DELIVERED_STATUS:[],
            PackageFields.TRANSIT_STATUS:[]
        }
        for package in self.assigned_packages.get_packages(): #get all the packages status and place in the correct keys list.
            status = self.getPackageStatus(package.ID, time)
            statuses[status].append(package)
        return statuses