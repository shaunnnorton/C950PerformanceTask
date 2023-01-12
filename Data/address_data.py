import csv
from Models.address import Address

class AddressData():
    @staticmethod
    def getAddresses(address_file: str) -> dict:
        addresses = dict()
        addresses[-1] = {}
        with open(address_file, "r") as adcsv:
            reader = csv.reader(adcsv)
            for i in range(8):
                reader.__next__()
            hubRow = reader.__next__()
            hubAddress = Address(0,"4001 South 700 East","84107")
            hubConnections = []
            for index, item in enumerate(hubRow[2:]):
                if item == '':
                    hubConnections.append((index, 10000.0))
                else:
                    hubConnections.append((index, float(item)))
            hubAddress.add_connections(hubConnections)
            addresses[0] = hubAddress
            addresses[-1][hubAddress.Street] = 0

            id_count = 1
            for row in reader:
                id=id_count
                address = row[1]
                street, ZIP = AddressData.parseAddress(address)
                new_address = Address(id,street,ZIP)

                connections=[]
                for index, item in enumerate(row[2:]):
                    if item == "":
                        connections.append((index, 10000.0))
                    else:
                        connections.append((index, float(item)))
                new_address.add_connections(connections)

                addresses[id] = new_address
                addresses[-1][street] = id
                id_count+=1
        return(addresses)




    @staticmethod
    def parseAddress(address: str) -> tuple:
        split_address = address.split("\n")
        address_street = split_address[0].strip()
        address_zip = split_address[1].strip("() ")

        return address_street, address_zip

