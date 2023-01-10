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



distance = packages.addresses[packages.addresses[-1][packages.select_package(20).ADDRESS]][0]
selectPackage.addPackage(packages.select_package(20),packages,assigned,Truck1,datetime(hour=8),distance)
while len(Truck1._PACKAGES) < 16:
    nextPackage = selectPackage.selectNextShortest(packages,packages.select_package(Truck1._PACKAGES[-1][0]).ADDRESS,packages.addresses)
    selectPackage.addPackage(nextPackage[0],packages,assigned,Truck1,datetime(hour=8),nextPackage[1])

print(Truck1._PACKAGES)

deadlines=list
for package in packages.get_packages:
    deadline = selectPackage.get_deadline(package)
    if deadline:
        deadlines.append((deadline, package))

deadlines.sort(key=lambda x: x[0])
print(deadlines)
Truck2 = Truck("Dave",2)
deadlined_packages = Packages()
for package in deadlines:
    deadlined_packages.insert_package(package[0])

firstPackage = selectPackage.selectNextShortest(deadlined_packages,deadlined_packages.addresses[0].STREET,deadlined_packages.addresses)
    
selectPackage.addPackage(firstPackage[0],deadlined_packages, assigned,Truck2,datetime(hour=8),firstPackage[1])
packages.delete_package(firstPackage[0].ID)   
    
    if len(Truck2._PACKAGES) < 16 and len(Truck2._PACKAGES) > 0:
        nextPackage = selectPackage.selectNextShortest(packages,packages.select_package(Truck1._PACKAGES[-1][0].ADDRESS),packages.addresses)
    selectPackage.addPackage(nextPackage[0],packages,assigned,Truck1,datetime(hour=8),nextPackage[1])




"""
Sample Deadline Logic. 





"""