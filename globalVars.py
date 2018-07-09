
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
    calcRunningTotal = None

    def __init__(self, calcRunningTotal):
        self.calcRunningTotal = calcRunningTotal
        print("calcRunningTotal class created")

    def setRunningTotal(self, calcRunningTotal):
        return self.calcRunningTotal

    def getRunningTotal(self):
        # print("getter = " + str(self.bankInfoDoesExist))
        return self.calcRunningTotal
