import datetime as dt

class Utils():

    @staticmethod
    def getDefaultDates()-> dt.datetime:
        beginDT = dt.now().date()
        openingTime = dt.datetime(hour=8)
        return beginDT, openingTime

    