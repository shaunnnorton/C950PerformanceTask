from datetime import datetime,timedelta

from Data.package_data import PackageFields

from Utils.delivery import Delivery




Planner = Delivery("Data/WGUPS Package File - Sheet1.csv","Data/DistanceTable - Sheet1.csv", timedelta(hours=8))
Planner.createRoutes()
Planner.deliverAll()

def promptUser() -> str:
    actions = ("++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
               "[1] Show Package Status                               \n" + 
               "[2] Show All Package Status                           \n" +
               "[3] Show Total Mileage                                \n" +
               "[4] Exit                                              \n" +
               "++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    select_action = input("What Action would you like to take? (Enter a number!) \n {actions}")
    match select_action.strip():
        case "1":
            package_input = input("Please input the package id:\t")
            time_input =  input("What time would you like to know the status at? (24hour format HH:MM):\t")
            package_id = None
            time = None
            try:
                package_id = int(package_id.strip())
                hours = int(time_input.strip()[::2])
                minutes = int(time_input.strip()[2:4])
                time = timedelta(hours=hours,minutes=minutes)
            except:
                print("There was an issue with the input")
                input("Please press ENTER to continue.....")
                return True
            status = Planner.getPackageStatus(package_id,time)
            match status:
                case PackageFields.HUB_STATUS:
                    print(f"Package: {package_id} is at the Hub at {time}!")
                case PackageFields.DELIVERED_STATUS:
                    print(f"Package: {package_id} is delivered at {time}!")
                case PackageFields.TRANSIT_STATUS:
                    print(f"Package: {package_id} is enroute at {time}!")

        case "2":
            time_input =  input("What time would you like to know the status at? (24hour format HH:MM):\t")
            time = None
            try:
                hours = int(time_input.strip()[::2])
                minutes = int(time_input.strip()[2:4])
                time = timedelta(hours=hours,minutes=minutes)
            except:
                print("There was an issue with the input")
                input("Please press ENTER to continue.....")
                return True
            all_statues = Planner.getAllPackageStatus(time)
            print("\n Packages at Hub \n")
            for package in all_statues[PackageFields.HUB_STATUS]:
                print(f"Package {package.ID} is at the Hub at {time}")
            print("\n Delivered Packages \n")
            for package in all_statues[PackageFields.DELIVERED_STATUS]:
                print(f"Package {package.ID} is delivered at {time}")
            print("\n Packages En Route \n")
            for package in all_statues[PackageFields.TRANSIT_STATUS]:
                print(f"Package {package.ID} is delivered at {time}")
        case "3":
            print(f"TRUCK 1 Traveled: {Planner.Truck1._DISTANCE_TRAVELED}")
            print(f"TRUCK 2 Traveled: {Planner.Truck2._DISTANCE_TRAVELED}")
            print(f"The combined total distance traveled was: {Planner.Truck1._DISTANCE_TRAVELED + Planner.Truck2._DISTANCE_TRAVELED}")
        case "4":
            return False
        case _:
            print("OPPS! That input was not recognized.")

    input("Press ENTER to continue......")
    return True

if __name__=="__main__":
    run = True
    while run:
        promptUser()