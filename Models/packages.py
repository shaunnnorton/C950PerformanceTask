
from package import Package
class Packages():
    hash_buckets = 20
    packages = []
    def __init__(self) -> None:
        for i in range(20):
            packages.append([])

    def insert_package(package: Package):
        index = Package.ID%20
        packages[index].append(package)

    def search_package(id: int) -> list:
        pass