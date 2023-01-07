import csv
from Models.address import Address

class AddressData():
    @staticmethod
    def getAddresss(address_file: str) -> dict:
        addresses = dict()
        addresses[-1] = {}
        with open(address_file, "r") as adcsv:
            reader = csv.reader(adcsv)
            for i in range(7):
                reader.next()
            id_count = 0
            for row in reader:
                id=id_count
                address = row[1]
                street, ZIP = parseAddress(address)
                new_address = Address(id,street,ZIP)

                connections=[]
                for index, item in enumerate(row[1:]):
                    if item == None:
                        connections.append((index, 10000.0))
                    else:
                        connections.append((index, float(item)))
                new_address.add_connections(connections)

                addresses[id] = new_address
                addresses[-1][street] = id
                id_count+=1
        return(addresses)





    def parseAddress(address: str) -> tuple:
        split_address = address.split("\n")
        address_street = split_address[0].strip()
        address_zip = split_address[1].strip("() ")

        return address_street, address_zip

