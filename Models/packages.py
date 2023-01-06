
from package import Package
class Packages():
    hash_buckets = 20
    packages = []

    def __init__(self) -> None:
        for i in range(self.hash_buckets):
            packages.append([])

    def insert_package(self, package: Package):
        index = Package.ID % self.hash_buckets
        self.packages[index].append(package)
        if len(self.packages[index]) > self.hash_buckets*1.5:
            self.resize_hash_table()

    def search_packages(self,id: int) -> list:
        bucket_index = id % self.hash_buckets
        for i in self.packages[bucket_index]:
            if i.ID != id:
                continue
            else:
                return i.toList()
        return []

    def delete_package(self, id: int):
        bucket_index = id % self.hash_buckets
        for i in self.packages[bucket_index]:
            if i.ID != id:
                continue
            else:
                self.packages[bucket_index].remove(i)


    def resize_hash_table(self):
        current_table = self.packages
        self.hash_buckets *= 2
        self.packages = [[] for i in range(self.hash_buckets)]
        for bucket in current_table:
            for item in bucket:
                self.insert_package(item)
