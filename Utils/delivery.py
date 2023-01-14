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
    
    # Truck1Leave = timedelta(hours=9, minutes=5)
    # Truck2Leave = timedelta(hours=8)
    
    Truck1Leave = timedelta(hours=8) 
    Truck2Leave = timedelta(hours=9, minutes=5)


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
        if len(self.deadlined_packages.get_packages()) > 0: #Check if there are still deadlined packages to adds
            for package in self.deadlined_packages.get_packages():
                if len(truck._PACKAGES[route-1]) < 16:
                    note = Actions.translateAction(package.NOTES, package.ID)
                    avalible, add = Actions.verifyAvalible(note,truck,departureTime,self.unassigned_packages)
                    group_add = list(add)
                    if avalible:
                        if len(group_add) > 0:
                            for id in group_add:
                                group_add.remove(id)
                                pk  = self.unassigned_packages.select_package(id)
                                pk.TransitTime = departureTime
                                truck._PACKAGES[route-1].append(pk)
                                self.unassigned_packages.delete_package(id)
                                self.assigned_packages.insert_package(pk)
                                self.deadlined_packages.delete_package(id)
                        else:
                            truck._PACKAGES[route-1].append(package)
                            package.TransitTime = departureTime
                            self.unassigned_packages.delete_package(package.ID)
                            self.assigned_packages.insert_package(package)
                            self.deadlined_packages.delete_package(package.ID)
            
        for package in self.unassigned_packages.get_packages():
            if len(truck._PACKAGES[route-1]) < 16:
                note = Actions.translateAction(package.NOTES, package.ID)
                avalible, group_add = Actions.verifyAvalible(note,truck,departureTime,self.unassigned_packages)
                if avalible:
                    if len(group_add) > 0:
                        for id in group_add:   
                            pk  = self.unassigned_packages.select_package(id)
                            pk.TransitTime = departureTime
                            truck._PACKAGES[route-1].append(pk)
                            self.unassigned_packages.delete_package(id)
                            self.assigned_packages.insert_package(pk)
                    else:
                        truck._PACKAGES[route-1].append(package)
                        package.TransitTime = departureTime
                        self.unassigned_packages.delete_package(package.ID)
                        self.assigned_packages.insert_package(package)
       
        
    def distanceToHub(self, truck: Truck, route: int) -> float:
        """Calculate a trucks distance to the hub at the end of a route"""
        final_package = truck.routes[route][-1][0] #Get the final package of the route
        final_address = final_package.ADDRESS #get the final packages addresss
        address_index = self.assigned_packages.addresses[-1][final_address] # get the index of the final address. 
        distance = self.assigned_packages.addresses[address_index].connections[0] # get the distance to the hub
        truck.routes[0].append(distance[1])
        return distance[1] # return the distance. 


    def createRoute(self, truck:Truck, route: int):
        looped_packages = Packages()
        deadlined_packages = Packages()
        truck.routes.append([]) #add the route to the routes list. 
        for package in truck._PACKAGES[route-1]:
            if selectPackage.get_deadline(package):
                deadlined_packages.insert_package(package)
            else:
                looped_packages.insert_package(package)
        first_package = Package(-1,"","","","","",PackageFields.TRANSIT_STATUS,0.0,"")
        soonest = timedelta(hours=24)
        address = 0
        for package in deadlined_packages.get_packages():
            deadline = selectPackage.get_deadline(package)
            if deadline == None or soonest == None:
                continue
            elif deadline < soonest:
                soonest = selectPackage.get_deadline(package)
                first_package = package
        if first_package.ID != -1:
            address = self.unassigned_packages.addresses[-1][first_package.ADDRESS]
            distance = self.unassigned_packages.addresses[address].connections[0][1]
            truck.routes[route].append((first_package, distance))
            deadlined_packages.delete_package(first_package.ID)
        while len(deadlined_packages.get_packages()) > 0:
            next = selectPackage.selectNextShortest(deadlined_packages,address, self.unassigned_packages.addresses)
            truck.routes[route].append(next)
            address = self.unassigned_packages.addresses[-1][next[0].ADDRESS]
            deadlined_packages.delete_package(next[0].ID)


        if first_package.ID == -1:
            address = 0

        while len(looped_packages.get_packages()) > 0:
            next = selectPackage.selectNextShortest(looped_packages, address, self.unassigned_packages.addresses)
            truck.routes[route].append(next)
            address = self.unassigned_packages.addresses[-1][next[0].ADDRESS]
            looped_packages.delete_package(next[0].ID)






    def createRoutes(self) -> None:
        """Creates all rotues needed to deliver all packages in 2 Trucks."""
        self.loadTruck(self.Truck1, self.Truck1Leave) #Load the trucks first route using the inital time
        self.loadTruck(self.Truck2, self.Truck2Leave) #Load the trucks first route using the inital time
        self.createRoute(self.Truck1, 1)
        self.createRoute(self.Truck2, 1)
        self.distanceToHub(self.Truck1,1) #get distance needed for the truck to return to the warehouse
        self.distanceToHub(self.Truck2,1) #get distance needed for the truck to return to the warehouse
        
        while len(self.unassigned_packages.get_packages()) > 0: #While there are still packages to add. 
            truck1_total = self.Truck1.getAllRoutesLength() #Calculate the total length of the route and distacne to come back 
            truck2_total = self.Truck2.getAllRoutesLength() #Calculate the total length of the route and distacne to come back
            if truck1_total < truck2_total: #Use the truck that comes back first I.E. Has the shortest total
                route = len(self.Truck1.routes)
                self.loadTruck(self.Truck1, timedelta(hours=truck1_total/18) + self.Truck1Leave) #load truck again, with new departure time. 
                self.createRoute(self.Truck1, route)
                self.distanceToHub(self.Truck1, route)
                 
            else:
                route = len(self.Truck2.routes)
                self.loadTruck(self.Truck2, timedelta(hours=truck1_total/18) + self.Truck2Leave) #load truck again, with new departure time. 
                self.createRoute(self.Truck2, route)
                self.distanceToHub(self.Truck2, route)



    def deliverAll(self):
        """Sets packages in every truck to delivered and populates their delivered time."""
        for index, route in enumerate(self.Truck1.routes[1::]):
            depart_Time = route[-1][0].TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck1.deliverPackages(depart_Time,self.delivered_packages,index+1) #Deliver the packges in the truck
            #self.Truck1._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck1,index+1) #add the distance to hub to the total distanct traveled
            

        for index, route in enumerate(self.Truck2.routes[1::]):
            depart_Time = route[-1][0].TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck2.deliverPackages(depart_Time,self.delivered_packages,index+1) #Deliver the packges in the truck
            #self.Truck2._DISTANCE_TRAVELLED += self.distanceToHub(self.Truck2,index+1) #add the distance to hub to the total distanct traveled

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