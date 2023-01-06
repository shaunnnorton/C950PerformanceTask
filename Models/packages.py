
from package import Package
class Packages():
    hash_buckets = 20
    packages = []

    def __init__(self) -> None:
        for i in range(20):
            packages.append([])

    def insert_package(self, package: Package):
        index = Package.ID%20
        self.packages[index].append(package)

    def search_packages(self,id: int) -> list:
        bucket_index = id%20
        for i in self.packages[bucket_index]:
            if i.ID != id:
                continue
            else:
                return i.toList()
        return []