def isEmpty(input): 
    return input == ''

def formatMoney(input): 
    return "${:,.2f}".format(input)


def getBalance(user):
    balance = 0
    if len(user["deposits"].values()) > 0:
        for i in user["deposits"].values():
            balance += i
    if len(user["withdrawls"].values()) > 0:
        for i in user["withdrawls"].values():
            balance -= i
    return balance