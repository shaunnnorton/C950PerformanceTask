from Data.package_data import PackageData
from Data.address_data import AddressData
from Utils.packageSelection import selectPackage
from datetime import datetime
#print(pd.PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv"))
# packages = pd.PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv")

# set_packages = packages.get_packages()
# package40 = packages.search_packages(40)
# #print(package40)


# addresses = ad.AddressData.getAddresss("Data/DistanceTable - Sheet1.csv")
# print(addresses[26].connections)


# for i in set_packages:
#     print(selectPackage.selectNextShortest(packages,i,addresses).ID)

beginDate = datetime.now().date()
openingTime = datetime(beginDate.year,beginDate.month, beginDate.day, 8, 0, 0, 0)
print(beginDate.strftime("%m %d %y %I %M"))
print(openingTime.strftime("%m %d %y %I %M"))