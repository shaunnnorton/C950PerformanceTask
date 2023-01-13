from datetime import datetime,timedelta

from Utils.delivery import Delivery


new_delivery = Delivery("Data/WGUPS Package File - Sheet1.csv","Data/DistanceTable - Sheet1.csv", timedelta(hours=8))
new_delivery.createRoutes()
new_delivery.deliverAll()

print(new_delivery.getAllPackageStatus(timedelta(hours=9)))