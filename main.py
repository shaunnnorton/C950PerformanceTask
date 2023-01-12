from Data.package_data import PackageData
from Data.address_data import AddressData
from Utils.packageSelection import selectPackage
from datetime import datetime
from Utils.specialNotes import Actions
from Models.packages import Packages
from Models.truck import Truck
from Utils.utils import Utils

from Utils.specialNotes import *
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
Truck1 = Truck("TED", 1)


# selectPackage.addPackage(packages.select_package(1),packages,assigned,Truck1,"SS")

# print(Truck1._PACKAGES)
# selectPackage.addPackage(packages.select_package(20),packages,assigned,Truck1,"SS")
# selectPackage.addPackage(packages.select_package(38),packages,assigned,Truck1,"SS")
# selectPackage.addPackage(packages.select_package(32),packages,assigned,Truck1,"SS")

print(Truck1._PACKAGES)

# print(addresses[26].connections)


# for i in set_packages:
#     print(selectPackage.selectNextShortest(packages,i,addresses).ID)

beginDate = datetime.now().date()
openingTime = datetime(beginDate.year,beginDate.month, beginDate.day, 8, 0, 0, 0)
print(beginDate.strftime("%m %d %y %I %M"))
print(openingTime.strftime("%m %d %y %I %M"))

day, opening = Utils.getDefaultDates()

#"""
#Sample Deadline Logic. 
deadlines=list()
for package in packages.get_packages():
    deadline = selectPackage.get_deadline(package)
    print(deadline)
    if deadline:
        deadlines.append((deadline, package))

deadlines.sort(key=lambda x: x[0])
print(deadlines)
Truck2 = Truck("Dave",2)
deadlined_packages = Packages()
for package in deadlines:
    deadlined_packages.insert_package(package[1])


print(deadlined_packages)

firstPackage = selectPackage.selectNextShortest(deadlined_packages,packages.addresses[0].Street,packages.addresses,Truck2,opening)
print(firstPackage)

selectPackage.addPackage(firstPackage[0],packages, assigned,Truck2,opening,firstPackage[1])
deadlined_packages.delete_package(firstPackage[0].ID) 
#deadlined_packages.delete_package()  
print(Truck2._PACKAGES)


while len(Truck2._PACKAGES) < 16 and len(Truck2._PACKAGES) > 0 and len(deadlined_packages.get_packages())>0:
    for package in packages.get_packages():
        print(f"{package.ID}  UNASSIGNED")
    for package in assigned.get_packages():
        print(f"{package.ID}  Assigned")
    testVar = False
    for i in packages.get_packages():
        note = Actions.translateAction(i.NOTES, i.ID)
        if Actions.verifyAvalible(note,Truck2,opening,packages)[0]:
            testVar = True
    if testVar == False:
        print(packages.get_packages())
        for package in packages.get_packages():
            print(package.ID)
        for package in assigned.get_packages():
            print(f"{package.ID}  Assigned")
        break
    print(testVar)
    nextPackage = selectPackage.selectNextShortest(packages,assigned.select_package(Truck2._PACKAGES[-1][0]).ADDRESS,packages.addresses,Truck2,opening)
    #print(deadlined_packages.get_packages())
    selectPackage.addPackage(nextPackage[0],packages,assigned,Truck2,opening,nextPackage[1])
    deadlined_packages.delete_package(nextPackage[0].ID)

print(Truck2._PACKAGES)
print("HERO")








distance = packages.addresses[packages.addresses[-1][packages.select_package(2).ADDRESS]].connections[0][1]
selectPackage.addPackage(packages.select_package(2),packages,assigned,Truck1,opening,distance)
failed = 0
while len(Truck1._PACKAGES) < 16:
    nextPackage = selectPackage.selectNextShortest(packages,assigned.select_package(Truck1._PACKAGES[-1][0]).ADDRESS,packages.addresses,Truck1,opening)
    if nextPackage[0] == None:
        break
    selectPackage.addPackage(nextPackage[0],packages,assigned,Truck1,opening,nextPackage[1])

print(Truck1._PACKAGES)








#"""