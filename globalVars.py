

class cl_HasBankInformation():
    bankInfoDoesExist = None

    def __init__(self, bankInfoDoesExist):
        self.bankInfoDoesExist = bankInfoDoesExist
        print("hasBankInfo class created")

    def setBankInformation(self, hasBankInfo):
        if hasBankInfo is True:
            print("setterTrue")
            bankInfoDoesExist = True
        elif hasBankInfo is False:
            print("setterFalse")
            bankInfoDoesExist = False
        else:
            print("setterNone")
            bankInfoDoesExist = None

    def getBankInformation(self):
        print("getter")
        return self.bankInfoDoesExist
