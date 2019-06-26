import datetime
import calendar

def addMonths(origDate, numMonths):
    # Advance year and month by one month
    newYear = origDate.year
    newMonth = origDate.month + numMonths
    # Note: in datetime.date, months go from 1 to 12
    if newMonth > 12:
        newYear += 1
        newMonth -= 12

    lastDayOfMonth = calendar.monthrange(newYear, newMonth)[1]
    newDay = min(origDate.day, lastDayOfMonth)

    return origDate.replace(year=newYear, month=newMonth, day=newDay)
