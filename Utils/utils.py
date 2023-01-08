import datetime as dt

class Utils():

    @staticmethod
    def getDefaultDates()-> datetime.datetime:
        beginDT = datetime.now().date()
        openingTime = datetime(beginDate.year,beginDate.month, beginDate.day, 8, 0, 0, 0)
        return beginDT, openingTime

    