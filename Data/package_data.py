import csv
from enum import Enum as e

class PackageFields(e):
    """Provides Standard values and enum for Package fields"""
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
    DELIVERED_STATUS = 200
    HUB_STATUS = 202
    TRANSIT_STATUS = 204

from Models.packages import Packages
from Models.package import Package

class PackageData():
    """Class to parse data from the package csv"""
    @staticmethod
    def getPackages(package_file) -> Packages:
        """Parses data from the packages CSV to create package objects in a packages hash table."""
        new_packages = Packages() #Create new packages object. 
        with open(package_file, "r") as pkcsv:
            reader = csv.reader(pkcsv)
            for i in range(7): #Skip the first seven rows of the CSV as the provide no useful information
                reader.__next__() 
            reader.__next__() #skip another row that provides the headers.
            for row in reader: #For each row create a new package and add it to the packages hash table.
                new_package = Package(int(row[PackageFields.ID_INDEX.value]),
                                        row[PackageFields.ADDRESS_INDEX.value],
                                        row[PackageFields.DEADLINE_INDEX.value],
                                        row[PackageFields.CITY_INDEX.value],
                                        row[PackageFields.STATE_INDEX.value],
                                        row[PackageFields.ZIP_INDEX.value],
                                        PackageFields.HUB_STATUS,
                                        float(row[PackageFields.MASS_INDEX.value]),
                                        row[PackageFields.SPNOTES_INDEX.value])
                new_packages.insert_package(new_package)
        return new_packages 
