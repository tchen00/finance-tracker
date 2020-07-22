class Record:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

class Ledger:
    def __init__(self, credits, debits):
        self.credits = credits
        self.debits = debits

class User:
    def __init__(self, userId, ledger):
        self.userId = userId
        self.ledger = ledger

def loadFromDB():
    