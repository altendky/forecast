from event import Event
from dateutil import relativedelta

class Annuity:
    def __init__(self, name, start, amount, period, periods=None, end=None):
        p = periods
        if periods == None and end == None:
            p = 1
        elif periods != None and end != None:
            end = None
        periods = p

        self.name = name
        self.start = start
        self.amount = amount
        self.period = period

        self.events = []

        date = start
        if periods:
            for periodIndex in range(1, periods):
                eventName = "{0} ({1} of {2})".format(self.name, periodIndex, periods)
                self.events.append(Event(name=eventName, date=date, amount=self.amount))
                date += period
        elif end:
            periodIndex = 1
            while date <= end:
                eventName = "{0} ({1} of {2})".format(self.name, periodIndex, periods)
                self.events.append(Event(name=eventName, date=date, amount=self.amount))
                date += period
                periodIndex += 1

    def getevents(self):
        return self.events

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
    
    def __mul__(self, other):
        new = self
        i = 0
        while i < len(new.events):
            new.events[i] *= other
            i += 1
        #for event in new.events:
            #event *= other
        return new

    def __neg__(self):
        return self * -1
    
    def __str__(self):
        return ": (" + self.amount.__str__() + ") " + self.name
