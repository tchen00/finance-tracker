"""class Record:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

class BalanceSht:
    def __init__(self, assets, liabilities):
        self.assets = assets
        self.liabilities = liabilities
    
    def print(self):
        for asset in self.assets:
            print(asset)
        
        for liability in self.liabilities:
            print(liability)
            
class User:
    def __init__(self, userId, balanceSht):
        self.userId = userId
        self.balanceSht = balanceSht
"""


def isEmpty(input): 
    return input == ''

def formatMoney(input): 
    return "${:,.2f}".format(input)