
from Models.package import Package

class Packages():
    """Class to provide hashtable functionality to sort and store packages."""
    addresses = {}


    def __init__(self) -> None:
        """Initializes hash table with 20 buckets"""
        self.hash_buckets = 20 #initial hash table size
        self.packages = [] #initialize hashtable with 0 buckets
        self.grouped_packages = []
        
        for i in range(self.hash_buckets): #create an empty list 20 times to serve as buckets.
            self.packages.append([])

    def insert_package(self, package: Package):
        """Inserts a Package Object into the hash table."""
        bucket = self.calculate_bucket(package.ID)
        self.packages[bucket].append(package) #Add the Package to the bucket
        if len(self.packages[bucket]) > self.hash_buckets*1.5: #Check if too many collisions in the table
            self.resize_hash_table() #Resize the table

    def search_packages(self,id: int) -> tuple:
        """Searches for a package with a matching id in the hash table."""
        bucket_index = self.calculate_bucket(id) #bucket index of the id
        for i in self.packages[bucket_index]:#Look through the bucket
            if i.ID != id:
                continue
            else:
                return i.toTuple() #return a list containing all the information of the package
        return tuple() #return an empty list if no Package is found

    

    def delete_package(self, id: int):
        """Removes a package from the hash table with a matching ID"""
        bucket_index = self.calculate_bucket(id) #calculate the bucket to search 
        for i in self.packages[bucket_index]: #find the package to remove
            if i.ID != id:
                continue
            else:
                self.packages[bucket_index].remove(i) #remove the package from the list if found. 

    def select_package(self, id: int) -> Package:
        """Searches for a package with a matching id in the hash table and returns the package."""
        bucket_index = self.calculate_bucket(id) #bucket index of the id
        for i in self.packages[bucket_index]:#Look through the bucket
            if i.ID != id:
                continue
            else:
                return i #return the package
        return None # type: ignore #return an empty list if no Package is found


    def get_packages(self):
        packages = set()
        for bucket in self.packages:
            for j in bucket:
                packages.add(j)
        return packages


    def resize_hash_table(self):
        """Resizes the hash table to double the amount of buckets and rehashes all items already in the hash table"""
        current_table = self.packages #store the current hash table
        self.hash_buckets *= 2 #double the amount of buckets
        self.packages = [[] for i in range(self.hash_buckets)] #Creates the hash table with the correct number of empty buckets
        for bucket in current_table: # Repopulates the hashtable with new hashes. 
            for item in bucket:
                self.insert_package(item)

    def calculate_bucket(self, id):
        """Calculatest the bucket in the hash table using an id"""
        return id % self.hash_buckets # Take the Mod of the id and the amount of buckets. 


    def setAddresses(self, addresses):
        self.addresses = addresses
    