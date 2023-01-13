import csv
from Models.address import Address

class AddressData():
    """Class to provide methods to extract data from a csv containing all the address data"""
    @staticmethod
    def getAddresses(address_file: str) -> dict:
        """Creates an Address object using each Addres row in the csv.
            Parameters:
                address_file (str) The path to the csv to extract data from
            returns: 
                dict: containing objects where the key is the address id and key "-1" provides and index for the street variable of the address.
        
        """
        addresses = dict() #init the address dictionary
        addresses[-1] = {} #init the dictionary to be used as an index of the street names.
        with open(address_file, "r") as adcsv: #open the csv file in read mode
            reader = csv.reader(adcsv)
            for i in range(8): #skip the first 8 rows in the csv as they are not useful. 
                reader.__next__()
            hubRow = reader.__next__() #set the hub row manually as it follows a different format than other rows. 
            hubAddress = Address(0,"4001 South 700 East","84107")
            hubConnections = [] #init the hubs connections property
            for index, item in enumerate(hubRow[2:]): #populat the hub connections
                if item == '': #if data is blank connection is to long to be viable.
                    hubConnections.append((index, 10000.0))
                else:
                    hubConnections.append((index, float(item)))
            hubAddress.add_connections(hubConnections)# add the connections to the hub
            #Add the hub to the address dict and index the street name
            addresses[0] = hubAddress
            addresses[-1][hubAddress.Street] = 0
            
            #Create the remaining addresses and connections from the rows in the csv. 
            id_count = 1 #start at Index/id 1
            for row in reader: #Loop through the rows. 
                id=id_count
                address = row[1]
                street, ZIP = AddressData.parseAddress(address)#parse the address data into a useable format. 
                new_address = Address(id,street,ZIP) #create address object. 

                connections=[] #init connections
                for index, item in enumerate(row[2:]):#add all connections from the remaining data 
                    if item == "": #default to distance of 10000.0 if no data
                        connections.append((index, 10000.0))
                    else:
                        connections.append((index, float(item)))
                new_address.add_connections(connections) #add the connection
                #add the new address to the dict and index the street name
                addresses[id] = new_address
                addresses[-1][street] = id
                id_count+=1
        return(addresses) #Return the addresses dict




    @staticmethod
    def parseAddress(address: str) -> tuple:
        "Parses an address string from the CSV into and street and zip code strings"
        split_address = address.split("\n") #split the provided data at the linebreak. 
        address_street = split_address[0].strip()#remove whitespace from the street portion
        address_zip = split_address[1].strip("() ")#remove parenthesis and whitspace from zip code portion.

        return address_street, address_zip

