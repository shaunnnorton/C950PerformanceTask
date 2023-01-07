import csv
from Models.address import Address

class AddressData():
    @staticmethod
    def getAddresss(address_file: str) -> dict:
        addresses = dict()
        with open(address_file, "r") as adcsv:
            reader = csv.reader(adcsv)
            for i in range(7):
                reader.next()
            id_count = 0
            for row in reader:
                id=id_count
                address = row[0]
                name,street,city,state,ZIP = parseAddress(address)
                new_address = Address(id,street,city,state,ZIP,name)

                connections=[]
                for index, item in enumerate(row[1:]):
                    if item == None:
                        connections.append((index, 10000.0))
                    else:
                        connections.append((index, float(item)))
                new_address.add_connections(connections)

                addresses[id] = new_address
        return(addresses)





    def parseAddress(address: str) -> tuple:
        split_address = address.split("\n")
        address_name = split_address[0].strip()
        address_street = split_address[1].strip()
        
        split_address = split_address[2].split(",")
        address_city = split_address[0].strip()

        split_address = split_address[1].split(" ")
        address_state = split_address[0].strip()
        address_zip = split_address[1].strip()
        return address_name,address_street,address_city,address_state, address_zip

