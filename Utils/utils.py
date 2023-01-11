import datetime as dt

class Utils():

    @staticmethod
    def getDefaultDates()-> tuple:
        todayDT = dt.datetime.today()
        openingTime = todayDT + dt.timedelta(hours=8)
        return todayDT, openingTime

    