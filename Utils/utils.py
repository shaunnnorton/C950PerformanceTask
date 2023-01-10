import datetime as dt

class Utils():

    @staticmethod
    def getDefaultDates()-> dt.datetime:
        beginDT = dt.now().date()
        openingTime = dt.datetime(beginDT.year,beginDT.month, beginDT.day, 8, 0, 0, 0)
        return beginDT, openingTime

    