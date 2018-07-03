

class cl_HasBankInformation():
    bankInfoDoesExist = None

    def __init__(self, bankInfoDoesExist):
        self.bankInfoDoesExist = bankInfoDoesExist
        print("hasBankInfo class created")

    def setBankInformation(self, hasBankInfo):
        if hasBankInfo is True:
            print("setterTrue")
            self.bankInfoDoesExist = True
        elif hasBankInfo is False:
            print("setterFalse")
            self.bankInfoDoesExist = False
        else:
            print("setterNone")
            self.bankInfoDoesExist = None

    def getBankInformation(self):
        print("getter = " + str(self.bankInfoDoesExist))
        return self.bankInfoDoesExist
