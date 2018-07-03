

class cl_HasBankInformation():
    bankInfoDoesExist = None

    def __init__(self, bankInfoDoesExist):
        self.bankInfoDoesExist = bankInfoDoesExist
        print("hasbankinfo class created")

    def setBankInformation(self, hasBankInfo):
        if hasBankInfo is True:
            print("setterTrue")
            bankInfoDoesExist = True
            return
        elif hasBankInfo is False:
            print("setterFalse")
            bankInfoDoesExist = False
            return
        else:
            print("setterNone")
            bankInfoDoesExist = None
            return

    def getBankInformation(self):
        print("getter")
        return bankInfoDoesExist
