import datetime as dt

class Utils():

    @staticmethod
    def getDefaultDates()-> tuple:
        "Return the default Date and opening time."
        todayDT = dt.datetime.today()
        openingTime = dt.timedelta(hours=8)
        return todayDT, openingTime

    