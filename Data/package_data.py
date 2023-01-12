import csv
from enum import Enum as e
from Models.packages import Packages
from Models.package import Package

class PackageFields(e):
    #Indexes in CSV
    ID_INDEX = 0
    ADDRESS_INDEX = 1
    CITY_INDEX = 2
    STATE_INDEX = 3
    ZIP_INDEX = 4
    DEADLINE_INDEX = 5
    MASS_INDEX = 6
    SPNOTES_INDEX = 7
    #Package Statues
    DELIVERED_STATUS = 0
    HUB_STATUS = 1
    TRANSIT_STATUS = 2



package_file = "Data/WGUPS Package File - Sheet1.csv"

class PackageData():
    # package_file = "Data/WGUPS Package File - Sheet1.csv"
    @staticmethod
    def getPackages(package_file) -> Packages:
        new_packages = Packages()
        with open(package_file, "r") as pkcsv:
            reader = csv.reader(pkcsv)
            for i in range(7):
                reader.__next__()
            reader.__next__()
            for row in reader:
                new_package = Package(int(row[PackageFields.ID_INDEX.value]),
                                        row[PackageFields.ADDRESS_INDEX.value],
                                        row[PackageFields.DEADLINE_INDEX.value],
                                        row[PackageFields.CITY_INDEX.value],
                                        row[PackageFields.STATE_INDEX.value],
                                        row[PackageFields.ZIP_INDEX.value],
                                        PackageFields.HUB_STATUS.value,
                                        float(row[PackageFields.MASS_INDEX.value]),
                                        row[PackageFields.SPNOTES_INDEX.value])
                new_packages.insert_package(new_package)
        return new_packages 
