

class cl_HasBankInformation():
    bankInfoDoesExist = None

    def __init__(self):
        print("hasbankinfo class created")

    def setBankInformation(hasBankInfo):
        if hasBankInfo is True:
            bankInfoDoesExist = True
            return
        elif hasBankInfo is False:
            bankInfoDoesExist = False
            return
        else:
            bankInfoDoesExist = None
            return

    def getBankInformation():
        return bankInfoDoesExist
