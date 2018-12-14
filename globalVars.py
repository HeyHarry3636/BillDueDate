import decimal, datetime
# Class to check if the user has bank information in the database already
class cl_HasBankInformation():
    bankInfoDoesExist = None

    def __init__(self, bankInfoDoesExist):
        self.bankInfoDoesExist = bankInfoDoesExist
        # print("hasBankInfo class created")

    def setBankInformation(self, hasBankInfo):
        if hasBankInfo is True:
            # print("setterTrue")
            self.bankInfoDoesExist = True
        elif hasBankInfo is False:
            # print("setterFalse")
            self.bankInfoDoesExist = False
        else:
            # print("setterNone")
            self.bankInfoDoesExist = None

    def getBankInformation(self):
        # print("getter = " + str(self.bankInfoDoesExist))
        return self.bankInfoDoesExist


# Method to calculate the runningTotal value for updating the bank table
class cl_calculateRunningTotal():
    calcRunningTotal = decimal.Decimal(0.00)

    def __init__(self, calcRunningTotal):
        self.calcRunningTotal = decimal.Decimal(calcRunningTotal)

    def setInitialAmount(self, runningTotalValue):
        self.calcRunningTotal = runningTotalValue
        return self.calcRunningTotal

    def setRunningTotal(self, runningTotalValue):
        self.calcRunningTotal = self.calcRunningTotal - runningTotalValue
        return self.calcRunningTotal

    def setRunningTotalAfterPayDay(self, runningTotalValue):
        self.calcRunningTotal = self.calcRunningTotal + 1706
        return self.calcRunningTotal

    def getRunningTotal(self):
        return self.calcRunningTotal


# Method to calculate the running 'date' for tracking remaining $ after bills
class cl_calculateRunningDate():
    calcRunningDate = datetime.datetime(1970, 1, 1)
    print("class type of calcRunningDate1 = " + str(type(calcRunningDate)))
    calcRunningDate = calcRunningDate.date()
    print("class type of calcRunningDate2 = " + str(type(calcRunningDate)))

    def __init__(self, calcRunningDate):
        self.calcRunningDate = calcRunningDate

    def convertDatetimeToDate(self, runningDateValue):
        self.calcRunningDate = runningDateValue.date()
        return self.calcRunningDate

    def setInitialDate(self, runningDateValue):
        self.calcRunningDate = runningDateValue
        return self.calcRunningDate

    def getRunningDate(self):
        return self.calcRunningDate
