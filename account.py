from event import Event

class Account:
    def __init__(self, name = "", start=None, end=None, period=None, interestRate=None):
        self.name = "<unspecified>"
        self.period = period
        self.start = start
        self.end = end
        self.interestRate = interestRate
        self.events = []
        if len(name) > 0:
            self.name = name

    def addevents(self, events):
        try:
            self.events.extend(events.getevents())
        except AttributeError:
            try:
                self.events.extend(events)
            except TypeError:
                self.events.append(events)

        self.events.sort

    def getevents(self):
        if self.interestRate != None:
            #lastEvent = None
            #periodEvents = []
            print(self.name)
            print(self.events)
            firstDate = sorted(self.events, key=lambda e: e.date)[0].date

            nextPeriod = self.start
            while nextPeriod <= self.end:
                if nextPeriod > firstDate:
                    self.events.append(Event("Interest", nextPeriod, 0))
                nextPeriod += self.period

            events = sorted(self.events, key=lambda e: e.date)
            i = 0
            balance = 0
            while i < len(events):
                if events[i].name == "Interest":
                    events[i].amount = balance * self.interestRate/100
                #print([self.interestRate, balance, events[i].amount], events[i].date)
                balance += events[i].amount
                i += 1
                
            #for event in sorted(self.events, key=lambda e: e.date):
                #balance += event.amount
                
                #if event.name == "Interest":
                    #event.amount = 
                    
                #if event.date < nextPeriod:
                    #periodEvents.append(event)
                #else
                    #for periodEvent in periodEvents:
                        #interestRate += 
                    
                    #for periodEvent in periodEvents:
                        #balance +=
                    #periodEvents = []
                    #nextPeriod += period
            
        return self.events
