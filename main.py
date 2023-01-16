
#SHAUN NORTON STUDENT ID: 010483427
###################################################################
#IDENTIFICAITON INFORMATION
#NAME: SHAUN NORTON
#STUDENT ID: 010483427
##################################################################

from datetime import timedelta
from time import sleep
from Data.package_data import PackageFields

from Utils.delivery import Delivery




Planner = Delivery("Data/WGUPS Package File - Sheet1.csv","Data/DistanceTable - Sheet1.csv", timedelta(hours=8)) #Time Complexity O(n^2):Space Complexity O(n^2) Create the delivery Object
Planner.createRoutes() # Time Complexity O(n^3):Space Complexity O(n^2) Create all the routes
Planner.deliverAll() # Time Complexity O(n^3):Space Complexity O(n^2) Deliver all the packages

def promptUser() -> bool:
    """Time Complexity O(n^2): Space Complexity O(n) Prompt the user for actions and display status"""
    actions = ("++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
               " [1] Show Package Status                               \n" + 
               " [2] Show All Package Status                           \n" +
               " [3] Show Total Mileage                                \n" +
               " [4] Show Truck Assignments                            \n" +
               " [5] Exit                                              \n" +
               " ++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    select_action = input(f"What Action would you like to take? (Enter a number!) \n {actions}")
    match select_action.strip():
        case "1":
            package_input = input("Please input the package id:\t")
            time_input =  input("What time would you like to know the status at? (24hour format HH:MM):\t")
            package_id = None
            time = None
            try:
                package_id = int(package_input.strip())
                hours = int(time_input.split(":")[0])
                minutes = int(time_input.split(":")[1])
                time = timedelta(hours=hours,minutes=minutes)
            except:
                print("There was an issue with the input")
                input("Please press ENTER to continue.....")
                return True

            print("\n Package info = (ID, Street address, Deadline, City, State, Zip Code, Status, Weight, Note)")

            status = Planner.getPackageStatus(package_id,time)
            package = status[1]
            match status[0]:
                case PackageFields.HUB_STATUS:
                    package_info = list(package.toTuple())
                    package_info[6] = "at the HUB"
                    print(f"Package {package.ID} is at the Hub at {time}. It will be delivered at: {package.TimeDelivered}. Package information: {package_info}.")
                case PackageFields.DELIVERED_STATUS:
                    package_info =  list(package.toTuple())
                    package_info[6] = "Delivered"
                    print(f"Package {package.ID} is delivered as of {time}. It was delivered at: {package.TimeDelivered}. Package information: {package_info}.")
                case PackageFields.TRANSIT_STATUS:
                    package_info =  list(package.toTuple())
                    package_info[6] = "en Route"
                    print(f"Package {package.ID} is en route as of {time}. It will be delivered at: {package.TimeDelivered}. Package information: {package_info}.")
        case "2":
            time_input =  input("What time would you like to know the status at? (24hour format HH:MM):\t")
            time = None
            try:
                hours = int(time_input.split(":")[0])
                minutes = int(time_input.split(":")[1])
                time = timedelta(hours=hours,minutes=minutes)
            except:
                print("There was an issue with the input")
                input("Please press ENTER to continue.....")
                return True
            all_statues = Planner.getAllPackageStatus(time) #O(n^2)
            print("\n Package info = (ID, Street address, Deadline, City, State, Zip Code, Status, Weight, Note)")
            print("\n Packages at Hub \n")
            for package in all_statues[PackageFields.HUB_STATUS]:
                package_info = list(package.toTuple())
                package_info[6] = "at the HUB"
                print(f"Package {package.ID} is at the Hub at {time}. It will be delivered at: {package.TimeDelivered}. Package information: {package_info}.")
            print("\n Delivered Packages \n")
            for package in all_statues[PackageFields.DELIVERED_STATUS]:
                package_info =  list(package.toTuple())
                package_info[6] = "Delivered"
                print(f"Package {package.ID} is delivered as of {time}. It was delivered at: {package.TimeDelivered}. Package information: {package_info}.")

            print("\n Packages En Route \n")
            for package in all_statues[PackageFields.TRANSIT_STATUS]:
                package_info =  list(package.toTuple())
                package_info[6] = "en Route"
                print(f"Package {package.ID} is en route as of {time}. It will be delivered at: {package.TimeDelivered}. Package information: {package_info}.")
        case "3":
            print(f"TRUCK 1 Traveled: {Planner.Truck1._DISTANCE_TRAVELLED}")
            print(f"TRUCK 2 Traveled: {Planner.Truck2._DISTANCE_TRAVELLED}")
            print(f"The combined total distance traveled was: {Planner.Truck1._DISTANCE_TRAVELLED + Planner.Truck2._DISTANCE_TRAVELLED}")
        case "4":
            t1_pk = []
            for i in Planner.Truck1.PACKAGES:
                for j in i:
                    t1_pk.append(f"Package {j.ID}")
            t2_pk = []
            for i in Planner.Truck2.PACKAGES:
                for j in i:
                    t2_pk.append(f"Package {j.ID}")
            print(f"TRUCK 1 DELIVERED: {t1_pk}")
            print(f"TRUCK 2 DELIVERED: {t2_pk}")
        case "5":
            return False
        case _:
            print("OPPS! That input was not recognized.")

    input("Press ENTER to continue......")
    return True

if __name__=="__main__":
    run = True
    while run:
        run = promptUser()