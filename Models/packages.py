
from Models.package import Package

class Packages():
    """Class to provide hashtable functionality to sort and store packages."""
    addresses = {}


    def __init__(self) -> None:
        """Time Complexity O(n):Space Complexity O(n) Initializes hash table with 20 buckets"""
        self.hash_buckets = 20 #initial hash table size
        self.packages = [] #initialize hashtable with 0 buckets
        self.grouped_packages = []
        
        for i in range(self.hash_buckets): #O(n) create an empty list 20 times to serve as buckets.
            self.packages.append([])

    def insert_package(self, package: Package):
        """Time Complexity O(n):Space Complexity O(n) Inserts a Package Object into the hash table."""
        bucket = self.calculate_bucket(package.ID)
        self.packages[bucket].append(package) #Add the Package to the bucket
        if len(self.packages[bucket]) > self.hash_buckets*1.5: #Check if too many collisions in the table
            self.resize_hash_table() #O(n) Resize the table

    def insert_new_package(self, ID, address, deadline, city, zipcode, weight, status):
        """Time Complexity O(n):Space Complexity O(n) Inserts a Package Object into the hash table."""
        package = Package(ID, address,deadline,city,"",zipcode,status,weight," | ")
        bucket = self.calculate_bucket(package.ID)
        self.packages[bucket].append(package) #Add the Package to the bucket
        if len(self.packages[bucket]) > self.hash_buckets*1.5: #Check if too many collisions in the table
            self.resize_hash_table() #O(n) Resize the table


    def search_packages(self,id: int) -> tuple:
        """Time Complexity O(n):Space Complexity O(1) Searches for a package with a matching id in the hash table."""
        bucket_index = self.calculate_bucket(id) #bucket index of the id
        for i in self.packages[bucket_index]:#O(n) Look through the bucket
            if i.ID != id:
                continue
            else:
                return i.toTuple() #return a list containing all the information of the package
        return tuple() #return an empty list if no Package is found

    

    def delete_package(self, id: int):
        """Time Complexity O(n):Space Complexity O(1) Removes a package from the hash table with a matching ID"""
        bucket_index = self.calculate_bucket(id) #calculate the bucket to search 
        for i in self.packages[bucket_index]: #O(n) find the package to remove
            if i.ID != id:
                continue
            else:
                self.packages[bucket_index].remove(i) #O(1) remove the package from the list if found. 

    def select_package(self, id: int) -> Package:
        """Time Complexity O(n):Space Complexity O(1) Searches for a package with a matching id in the hash table and returns the package."""
        bucket_index = self.calculate_bucket(id) #bucket index of the id
        for i in self.packages[bucket_index]:#O(n) Look through the bucket
            if i.ID != id:
                continue
            else:
                return i #return the package
        return None # type: ignore #return an empty list if no Package is found


    def get_packages(self):
        """Time Complexity O(n):Space Complexity O(n) Returns all packages in the has table as a list"""
        packages = list()
        for bucket in self.packages:#O(n) Iterate through each bucket in the hash table. 
            for j in bucket: #O(1) Iterate through the bucket adding the package to the list
                packages.append(j)
        return packages #retur the list of all packages.


    def resize_hash_table(self):
        """Time Complexity O(n):Space Complexity O(n))Resizes the hash table to double the amount of buckets and rehashes all items already in the hash table"""
        current_table = self.packages #store the current hash table
        self.hash_buckets *= 2 #double the amount of buckets
        self.packages = [[] for i in range(self.hash_buckets)] #Creates the hash table with the correct number of empty buckets
        for bucket in current_table: #O(n) Repopulates the hashtable with new hashes. 
            for item in bucket: # O(1)
                self.insert_package(item) #O(1)

    def calculate_bucket(self, id):
        """Time Complexity O(1):Space Complexity O(1) Calculatest the bucket in the hash table using an id"""
        return id % self.hash_buckets # Take the Mod of the id and the amount of buckets. 


    def setAddresses(self, addresses):
        """Time Complexity O(1):Space Complexity O(1) Sets the addreses variable of the hash table"""
        self.addresses = addresses
    