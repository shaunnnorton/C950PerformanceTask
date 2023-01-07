import csv
from Models.address import Address

class AddressData():
    @staticmethod
    def getAddresss(address_file) -> set:
        with open(address_file, "r") as adcsv:
            reader = csv.reader(adcsv)
            
