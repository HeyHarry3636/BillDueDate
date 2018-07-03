

class cl_HasBankInformation():
    bankInfoDoesExistasdf = None

    def __init__(self, bankInfoDoesExistasdf):
        self.bankInfoDoesExistasdf = bankInfoDoesExistasdf
        print("hasbankinfo class created")

    def setBankInformation(self, hasBankInfo):
        if hasBankInfo is True:
            bankInfoDoesExist = True
            return
        elif hasBankInfo is False:
            bankInfoDoesExist = False
            return
        else:
            bankInfoDoesExist = None
            return

    def getBankInformation(self):
        return bankInfoDoesExist
