from Data.package_data import PackageData
from Data.address_data import AddressData
from Utils.packageSelection import selectPackage
from datetime import datetime
from Utils.specialNotes import Actions
from Models.packages import Packages
from Models.truck import Truck
#print(pd.PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv"))
packages = PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv")
addresses = AddressData.getAddresss("Data/DistanceTable - Sheet1.csv")
packages.setAddresses(addresses)


set_packages = packages.get_packages()
# package40 = packages.search_packages(40)
# #print(package40)

Actions.groupPackages(packages)
print(packages.grouped_packages)

assigned = Packages()
Truck1 = Truck()


selectPackage.addPackage(packages.select_package(1),packages,assigned,Truck1,"SS")

print(Truck1._PACKAGES)
selectPackage.addPackage(packages.select_package(20),packages,assigned,Truck1,"SS")
selectPackage.addPackage(packages.select_package(38),packages,assigned,Truck1,"SS")
selectPackage.addPackage(packages.select_package(32),packages,assigned,Truck1,"SS")

print(Truck1._PACKAGES)

# print(addresses[26].connections)


# for i in set_packages:
#     print(selectPackage.selectNextShortest(packages,i,addresses).ID)

beginDate = datetime.now().date()
openingTime = datetime(beginDate.year,beginDate.month, beginDate.day, 8, 0, 0, 0)
print(beginDate.strftime("%m %d %y %I %M"))
print(openingTime.strftime("%m %d %y %I %M"))