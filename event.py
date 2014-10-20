import copy

class Event:
    def __init__(self, name, date, amount, credit=None, debit=None):
        self.name = name
        self.date = date
        self.amount = amount
        self.credit = credit
        self.debit = debit

    def __str__(self):
        return self.date.isoformat() + ": (" + self.amount.__str__() + ") " + self.name

    def __mul__(self, other):
        new = copy.copy(self)
        new.amount *= other
        return new

    def __neg__(self):
        return self * -1

    def addto(self, credit=None, debit=None):
        try:
            credit.addevents(self)
        except AttributeError:
            pass
        try:
            debit.addevents(-self)
        except AttributeError:
            pass
        return self
