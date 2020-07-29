def isEmpty(input): 
    return input == ''

def formatMoney(input): 
    return "${:,.2f}".format(input)


def getBalance(user):
    balance = 0
    
    for i in user["deposits"].values():
        balance += i

    for i in user["withdrawls"].values():
        balance -= i
    return balance