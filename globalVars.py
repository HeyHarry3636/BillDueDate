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


# # Method to calculate the runningTotal value for updating the bank table
# class cl_calculateRunningTotal():
#     calcRunningTotal = decimal.Decimal(0.00)
#
#     def __init__(self, calcRunningTotal):
#         self.calcRunningTotal = decimal.Decimal(calcRunningTotal)
#
#     def setInitialAmount(self, runningTotalValue):
#         self.calcRunningTotal = runningTotalValue
#         return self.calcRunningTotal
#
#     def setRunningTotal(self, runningTotalValue):
#         self.calcRunningTotal = self.calcRunningTotal - runningTotalValue
#         return self.calcRunningTotal
#
#     def setRunningTotalAfterPayDay(self, runningTotalValue):
#         self.calcRunningTotal = self.calcRunningTotal + round(decimal.Decimal(1774.15), 2)
#         return self.calcRunningTotal
#
#     def setRunningTotalAfterPayDayMultiple(self, runningTotalValue, payMultiplier):
#         self.calcRunningTotal = self.calcRunningTotal + (round(decimal.Decimal(1774.15), 2) * payMultiplier)
#         return self.calcRunningTotal
#
#     def getRunningTotal(self):
#         return self.calcRunningTotal

# Method to calculate the runningTotal value for updating the bank table
class cl_calculateRunningTotal():
    calcRunningTotal = decimal.Decimal(0.00)
    inputtedPayDayAmount = decimal.Decimal(0.00)

    def __init__(self, calcRunningTotal):
        self.calcRunningTotal = decimal.Decimal(calcRunningTotal)
        self.inputtedPayDayAmount = decimal.Decimal(inputtedPayDayAmount)

    def setInitialAmount(self, runningTotalValue):
        self.calcRunningTotal = runningTotalValue
        return self.calcRunningTotal

    def setRunningTotal(self, runningTotalValue):
        self.calcRunningTotal = self.calcRunningTotal - runningTotalValue
        return self.calcRunningTotal

    def setRunningTotalAfterPayDay(self, runningTotalValue, inputtedPayDayAmount):
        self.calcRunningTotal = self.calcRunningTotal + round(self.inputtedPayDayAmount, 2)

        return self.calcRunningTotal

    def setRunningTotalAfterPayDayMultiple(self, runningTotalValue, inputtedPayDayAmount, payMultiplier):
        self.calcRunningTotal = self.calcRunningTotal + (round(self.inputtedPayDayAmount, 2) * payMultiplier)
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
