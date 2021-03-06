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
class cl_calculatePayDayAmount():
    calcPayDayAmount = decimal.Decimal(0.00)

    def __init__(self, calcPayDayAmount):
        self.calcPayDayAmount = decimal.Decimal(calcPayDayAmount)

    def setPayDayAmount(self, inputtedPayDayAmount):
        self.calcPayDayAmount = inputtedPayDayAmount
        return self.calcPayDayAmount

    def getPayDayAmount(self):
        return self.calcPayDayAmount


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

    def setRunningTotalAfterPayDay(self, runningTotalValue, payDayInputAmount):
        self.calcRunningTotal = self.calcRunningTotal + round(payDayInputAmount, 2)
        return self.calcRunningTotal

    def setRunningTotalAfterPayDayMultiple(self, runningTotalValue, payDayInputAmount, payMultiplier):
        self.calcRunningTotal = self.calcRunningTotal + (round(payDayInputAmount, 2) * payMultiplier)
        return self.calcRunningTotal

    def getRunningTotal(self):
        return self.calcRunningTotal


# Method to calculate the running 'date' for tracking remaining $ after bills
class cl_calculateRunningDate():
    calcRunningDate = datetime.datetime(1970, 1, 1)

    def __init__(self, calcRunningDate):
        self.calcRunningDate = calcRunningDate

    def setInitialDate(self, runningDateValue):
        self.calcRunningDate = runningDateValue
        return self.calcRunningDate

    def getRunningDate(self):
        return self.calcRunningDate


# Method to calculate the number of months to project on screen
class cl_projectedMonths():
    projectedMonths = int(0)

    def __init__(self, projectedMonths):
        self.projectedMonths = projectedMonths

    def setProjectedMonths(self, projMon):
        self.projectedMonths = projMon
        return self.projectedMonths

    def getProjectedMonths(self):
        return self.projectedMonths
