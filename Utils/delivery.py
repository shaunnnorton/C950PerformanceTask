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
    
    Truck1Leave = timedelta(hours=9, minutes=5)
    Truck2Leave = timedelta(hours=8)
    
    # Truck1Leave = timedelta(hours=8) 
    # Truck2Leave = timedelta(hours=9, minutes=30)


    def __init__(self, package_csv: str, addresses_csv: str, initialTime: timedelta) -> None:
        """Time Complexity O(n^2):Space Complexity O(n^2) INIT all variables and populate packages and addressses"""
        self.unassigned_packages = PackageData.getPackages(package_csv)
        
        addresses = AddressData.getAddresses(addresses_csv) # Time complexity O(n^2): Space Complexity O(n^2)
        self.unassigned_packages.setAddresses(addresses)
        self.assigned_packages.setAddresses(addresses)
        self.delivered_packages.setAddresses(addresses)
        
        Actions.groupPackages(self.unassigned_packages) #Time Complexity O(n^2): Space Complexity O(n^2)

        self.hubAddress = addresses[0]

        for package in self.unassigned_packages.get_packages():# O(n) Add all packages with a deadline to deadlined packages
            deadline = selectPackage.get_deadline(package)
            if deadline:
                self.deadlined_packages.insert_package(package) #O(n)
        self.deadlined_packages.setAddresses(addresses)

        self.initial_time = initialTime


    def loadTruck(self, truck: Truck, departureTime: timedelta):
        """ Time Complexity O(n^2):Space Complexity O(n^2) Loads packages starting with deadlined packages into a truck"""
        route = len(truck.getPackages())+1 #Get the new route number. 
        truck.PACKAGES.append([])
        if len(self.deadlined_packages.get_packages()) > 0: #Check if there are still deadlined packages to adds
            for package in self.deadlined_packages.get_packages(): #O(n) + O(n) Check all the packages that have a deadline
                if len(truck.PACKAGES[route-1]) < 16: #If there is a room on a truck
                    note = Actions.translateAction(package.NOTES, package.ID) #Get the special note
                    avalible, add = Actions.verifyAvalible(note,truck,departureTime,self.unassigned_packages) #Verify the package is avalible
                    group_add = list(add) #Get other packages to add with this package
                    if avalible: #If the package is avalible
                        if len(group_add) > 0: #If other packagages have to be added. 
                            for id in group_add: #O(n) Add all the packages that must be added together.
                                group_add.remove(id) #Remove the id from the packages to add. 
                                pk  = self.unassigned_packages.select_package(id) # O(n) get the package object to all
                                pk.TransitTime = departureTime #set the packages intransit time
                                truck.PACKAGES[route-1].append(pk) #add the package to the truck. 
                                self.unassigned_packages.delete_package(id) # O(n) remove the package from unassigned packages
                                self.assigned_packages.insert_package(pk) # O(n) add the pakcage to tha assigned packages. 
                                self.deadlined_packages.delete_package(id) # O(n) remove the packages from the deadlined packages.
                        else:
                            truck.PACKAGES[route-1].append(package)
                            package.TransitTime = departureTime
                            self.unassigned_packages.delete_package(package.ID) # O(n) remove the package from unassigned packages
                            self.assigned_packages.insert_package(package) # O(n) add the pakcage to tha assigned packages. 
                            self.deadlined_packages.delete_package(package.ID) # O(n) remove the packages from the deadlined packages.
            
        for package in self.unassigned_packages.get_packages(): #O(n)*O(n^3) + O(n^2) Check all the packages that are unassigned
            if len(truck.PACKAGES[route-1]) < 16: #If there is a room on a truck
                note = Actions.translateAction(package.NOTES, package.ID) #Get the special note
                avalible, group_add = Actions.verifyAvalible(note,truck,departureTime,self.unassigned_packages) #Verify the package is avalible
                if avalible: #If the package is avalible
                    if len(group_add) > 0: #If other packagages have to be added. 
                        for id in group_add: #O(n) Add all the packages that must be added together.   
                            pk  = self.unassigned_packages.select_package(id) # O(n) get the package object to all
                            pk.TransitTime = departureTime #set the packages intransit time
                            truck.PACKAGES[route-1].append(pk) #add the package to the truck.
                            self.unassigned_packages.delete_package(id) # O(n) remove the package from unassigned packages
                            self.assigned_packages.insert_package(pk) # O(n^2) add the pakcage to tha assigned packages. 
                    else:
                        truck.PACKAGES[route-1].append(package) #add the package to the truck.
                        package.TransitTime = departureTime  #set the packages intransit time
                        self.unassigned_packages.delete_package(package.ID) # O(n) remove the package from unassigned packages
                        self.assigned_packages.insert_package(package) # O(n^2) add the pakcage to tha assigned packages. 
       
        
    def distanceToHub(self, truck: Truck, route: int) -> float:
        """Time Complexity O(1):Space Complexity O(1) Calculate a trucks distance to the hub at the end of a route"""
        final_package = truck.routes[route][-1][0] #Get the final package of the route
        final_address = final_package.ADDRESS #get the final packages addresss
        address_index = self.assigned_packages.addresses[-1][final_address] # get the index of the final address. 
        distance = self.assigned_packages.addresses[address_index].connections[0] # get the distance to the hub
        truck.routes[0].append(distance[1])
        return distance[1] # return the distance. 


    def createRoute(self, truck:Truck, route: int):
        """Time Complexity O(n^2):Space Complexity O(n^2) Creates a route using the nearest neighbor algoritm and the packages loaded into the truck for the route"""
        looped_packages = Packages() #O(n) create temporary object
        deadlined_packages = Packages() #O(n) create temporary object
        truck.routes.append([]) #add the route to the routes list. 
        for package in truck.PACKAGES[route-1]: #O(n) Sort the packages in the truck between deadlined and not deadlined
            if selectPackage.get_deadline(package):
                deadlined_packages.insert_package(package) #O(n)
            else:
                looped_packages.insert_package(package) #O(n^2)
        first_package = Package(-1,"","","","","",PackageFields.TRANSIT_STATUS,0.0,"") #init a tempoary Package
        soonest = timedelta(hours=24)
        address = 0
        for package in deadlined_packages.get_packages(): #O(n) + O(n^2) loop through all the packages with a deadline and get the lowest deadline
            deadline = selectPackage.get_deadline(package)  #get the deadline of the package
            if deadline == None or soonest == None:
                continue
            elif deadline < soonest: #set the package as the first package if it has the soonest deadline
                soonest = selectPackage.get_deadline(package) 
                first_package = package
        if first_package.ID != -1: #Checks if there were no deadlined packages adds the first package otherwise
            address = self.unassigned_packages.addresses[-1][first_package.ADDRESS] #Get the address ID
            distance = self.unassigned_packages.addresses[address].connections[0][1] #Get the distance to the package
            truck.routes[route].append((first_package, distance)) #add to the truck 
            deadlined_packages.delete_package(first_package.ID) #O(n) remove the package from the deadlined packages hash table
        while len(deadlined_packages.get_packages()) > 0: # O(n) + O(n) Add the rest of the deadlined packages
            next = selectPackage.selectNextShortest(deadlined_packages,address, self.unassigned_packages.addresses) # O(n) get the next package to add
            truck.routes[route].append(next) #add to the truck 
            address = self.unassigned_packages.addresses[-1][next[0].ADDRESS] #set the next address
            deadlined_packages.delete_package(next[0].ID) # O(n) remove the package from the iterative list


        if first_package.ID == -1: #Check if there were deadlined packages
            address = 0 #set the address to the hub otherwise

        while len(looped_packages.get_packages()) > 0:# O(n) + O(n) loop until the rest of the packages are added to a route
            next = selectPackage.selectNextShortest(looped_packages, address, self.unassigned_packages.addresses) # O(n) select the next closest package
            truck.routes[route].append(next) #add to the truck 
            address = self.unassigned_packages.addresses[-1][next[0].ADDRESS] #set the next address
            looped_packages.delete_package(next[0].ID) #O(n)remove the package from the iterative list






    def createRoutes(self) -> None:
        """ Time Complexity O(n^3):Space Complexity O(n^2) Creates all rotues needed to deliver all packages in 2 Trucks."""
        self.loadTruck(self.Truck1, self.Truck1Leave) # O(n^2) Load the trucks first route using the inital time
        self.loadTruck(self.Truck2, self.Truck2Leave) # O(n^2) Load the trucks first route using the inital time
        self.createRoute(self.Truck1, 1) # O(n^2) Create route 1
        self.createRoute(self.Truck2, 1) # O(n^2) Create rotue 1
        self.distanceToHub(self.Truck1,1) #get distance needed for the truck to return to the warehouse
        self.distanceToHub(self.Truck2,1) #get distance needed for the truck to return to the warehouse
        
        while len(self.unassigned_packages.get_packages()) > 0: #O(n) + O(n^2)While there are still packages to add. 
            truck1_total = self.Truck1.getAllRoutesLength() # O(n^2) Calculate the total length of the route and distacne to come back 
            truck2_total = self.Truck2.getAllRoutesLength() # O(n^2) Calculate the total length of the route and distacne to come back
            if truck1_total < truck2_total: #Use the truck that comes back first I.E. Has the shortest total
                route = len(self.Truck1.routes) #Get the route number
                self.loadTruck(self.Truck1, timedelta(hours=truck1_total/18) + self.Truck1Leave) # O(n^2) load truck again, with new departure time. 
                self.createRoute(self.Truck1, route) # O(n^2) create the next route
                self.distanceToHub(self.Truck1, route) #add the next distance to the hub
                 
            else:
                route = len(self.Truck2.routes)
                self.loadTruck(self.Truck2, timedelta(hours=truck1_total/18) + self.Truck2Leave) # O(n^4) load truck again, with new departure time. 
                self.createRoute(self.Truck2, route) # O(n^3) create the next route
                self.distanceToHub(self.Truck2, route) #add the next distance to the hub



    def deliverAll(self):
        """ Time Complexity O(n^3):Space Complexity O(n^2) Sets packages in every truck to delivered and populates their delivered time."""
        for index, route in enumerate(self.Truck1.routes[1::]): #O(n) Iterate through all routes
            depart_Time = route[-1][0].TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck1.deliverPackages(depart_Time,self.delivered_packages,index+1) # O(n^2) Deliver the packges in the truck

        for index, route in enumerate(self.Truck2.routes[1::]): #O(n) Iterate through all routes
            depart_Time = route[-1][0].TransitTime #Set the depart time to the depart time of the first package in the route
            self.Truck2.deliverPackages(depart_Time,self.delivered_packages,index+1) # O(n^2) Deliver the packges in the truck
        self.Truck1._DISTANCE_TRAVELLED -= self.Truck1.routes[0][-1] #Subtract the final distance to the hub as the trucks do not need to return 
        self.Truck2._DISTANCE_TRAVELLED -= self.Truck2.routes[0][-1] #Subtract the final distance to the hub as the trucks do not need to return 


    def getPackageStatus(self, id: int, time: timedelta) -> tuple[PackageFields,Package]:
        """Time Complexity O(n):Space Complexity O(1) Get the status of a package at a specific time"""
        package = self.delivered_packages.select_package(id) #O(n) Get the package
        transit = package.TransitTime #Get the packages transit time
        delivered = package.TimeDelivered #get the packages time deliverd
        if time < transit: #If time is before the time it is in transit it is at the hub
            return PackageFields.HUB_STATUS , package
        elif time >= transit and time < delivered: #If the time is between transit and deliverd it is in transit
            return PackageFields.TRANSIT_STATUS , package
        else: #Otherwise the package is in a delivered status
            return PackageFields.DELIVERED_STATUS, package

    def getAllPackageStatus(self, time) -> dict:
        """Time Complexity O(n^2):Space Complexity O(n) Gets all the packages statuses at a time"""
        statuses = {
            PackageFields.HUB_STATUS:[],
            PackageFields.DELIVERED_STATUS:[],
            PackageFields.TRANSIT_STATUS:[]
        }
        for package in self.assigned_packages.get_packages(): #O(n) + O(n^2)get all the packages status and place in the correct keys list.
            status = self.getPackageStatus(package.ID, time) #O(n) Get the status of the package
            statuses[status[0]].append(package)
        return statuses