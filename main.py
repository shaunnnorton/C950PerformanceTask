import Data.package_data as pd
import Data.address_data as ad
from Utils.packageSelection import selectPackage

#print(pd.PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv"))
packages = pd.PackageData.getPackages("Data/WGUPS Package File - Sheet1.csv")

set_packages = packages.get_packages()
package40 = packages.search_packages(40)
#print(package40)


addresses = ad.AddressData.getAddresss("Data/DistanceTable - Sheet1.csv")
print(addresses[26].connections)


for i in set_packages:
    print(selectPackage.selectNextShortest(packages,i,addresses).ID)