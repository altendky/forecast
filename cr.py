#!/usr/bin/env python3

# export f=budget-2014.03.30; export t=$(mktemp -d); libreoffice "-env:UserInstallation=file://$t" --headless --convert-to csv $f.ods; mv $f.csv budget.csv; rm -rf $t

from account import Account
from event import Event
import datetime
from dateutil.relativedelta import relativedelta
from annuity import Annuity

import collections

import matplotlib.pyplot as plt

import csv
import sys
import os

class Scenario():
    def __init__(self, csv_path=None):
        f = open(csv_path)
        
        self.vars = {}
        self.vars["Plot"] = {}
        while True:
            line = f.readline()
            noise = "\n, "
            a = line.rstrip(noise).lstrip(noise).split(",", 1)
            print(a)
            key = a[0]
            value = a[1]
            if key == "#":
                break;
            elif len(key) > 0:
                value = value.split(",")
                if key == "Plot":
                    print("888 - " + str(self.vars))
                    print("888 - " + str(self.vars["Plot"]))
                    print("888 - " + str(value))
                    print("888 - " + value[0])
                    self.vars["Plot"][value[0]] = value[1]
                    #print("888 - " + str(value))
                    #try:
                        #self.vars[key].append([value[0], value[1]])
                    #except:
                        #self.vars[key] = [value[0], value[1]]
                else:
                    if len(value) == 1:
                        value = value[0]
                    self.vars[key] = value

        #print(self.vars)

        self.accounts = {}
        for account in self.vars["Accounts"]:
            self.accounts[account] = Account(name=account)

        c = csv.DictReader(f)
        for l in c:
            if len(l["Name"]) == 0 or l["Name"][0] == '#' or len(l["#"]) > 0:
                continue
            print(l)
            creditAccount = self.accounts[l["Credit"]] if len(l["Credit"]) > 0 else None
            debitAccount = self.accounts[l["Debit"]] if len(l["Debit"]) > 0 else None
            name = l["Name"]
            print(self.vars)
            start = datetime.datetime.strptime(l["Start"], self.vars["Format"]) if len(l["Start"]) > 0 else None
            amount = float(l["Amount"]) if len(l["Amount"]) > 0 else None
            interestRate = float(l["Interest Rate"]) if len(l["Interest Rate"]) > 0 else None

            periods = ["Years", "Months", "Weeks", "Days"]
            period = relativedelta()
            for p in periods:
                try:
                    #print(p + " - >" + l[p] + "<")
                    l[p] = int(l[p])
                except (ValueError, TypeError):
                    l[p] = 0
            period = relativedelta(years=l["Years"], months=l["Months"], weeks=l["Weeks"], days=l["Days"])
            
            try:
                end = datetime.datetime.strptime(l["End"], self.vars["Format"])
            except ValueError:
                pass

            if l["Type"] == "Annuity":
                #print(l["Credit"])
                #print(l["Debit"])
                
                event = Annuity(name=name, start=start, end=end, amount=amount, period=period)
                #print(name)
                #print(start)
                #print(end)
                #print(amount)
                #print(period)
                #print(len(es.getevents()))
                #print(len(creditAccount.getevents()))
                #for account in self.vars["Accounts"]:
                    #print self.accounts[account].events
            elif l["Type"] == "Single":
                event = Event(name=name, date=start, amount=amount)
                try:
                    print(creditAccount.name)
                except (AttributeError):
                    pass
                try:
                    print(debitAccount.name)
                except (AttributeError):
                    pass
            elif l["Type"] == "Account":
                account = self.accounts[name] if len(name) > 0 else None
                account.interestRate = interestRate
                account.period = period
                account.start = start
                account.end = end
                continue
            else:
                raise Exception('Unknown account type <{}>'.format(l["Type"]))
            print(" - - - - - - - - - - : ")
            print(event)
            event.addto(credit=creditAccount, debit=debitAccount)
        f.close()

        #for a in self.accounts:
            #print("aaaa " + self.accounts[a].name)
            #print("aaaa " + str(len(self.accounts[a].getevents())))


        #print(datetime.datetime.strptime("2012.03.06", "%Y.%M.%d"))
        #Annuity(name="Kyle's paycheck", start=datetime.date(2012, 01, 19), amount=750, period=relativedelta(weeks=1), end=end).addto(credit=general)
        #Annuity(name="Kelly's paycheck", start=datetime.date(2012, 01, 25), amount=1780, period=relativedelta(weeks=2), end=end).addto(credit=general)
    
    def plot(self):
        fig = plt.figure()
        subplot = 0
        requested_subplots = sorted(set(self.vars["Plot"].values()))
        print("aaa " + str(requested_subplots))
        subplots = len(requested_subplots)
        print(requested_subplots)
        print(list(range(1,subplots+1)))
        subplot_indexes = dict(map(lambda *a:a,requested_subplots,list(range(1,subplots+1))))
        print("bbb " + str(subplot_indexes))

        #xlim_min = min([self.accounts[n].start for n in self.vars["Plot"] if self.accounts[n].start is not None])
        #xlim_max = max([self.accounts[n].end   for n in self.vars["Plot"] if self.accounts[n].end   is not None])
        start = datetime.datetime.strptime(self.vars["Start"], self.vars["Format"])
        end = datetime.datetime.strptime(self.vars["End"], self.vars["Format"])

        print("999 - " + str(self.vars["Plot"]))
        od = collections.OrderedDict(sorted(self.vars["Plot"].items()))
        for name, subplot in od.items():
            #print(plot)
            #name = plot[0]
            #subplot = plot[1]
            
            print("000 - subplots " + str(subplots))
            print("000 - subplots " + str(subplot))
            ax = fig.add_subplot(subplots, 1, subplot_indexes[subplot])
            #print("plotting " + name + " " + self.accounts[name].name + " " + str(len(self.accounts[name].getevents())))
            #plt.title(name)
            v = []
            t = []
            d = []
            for e in sorted(self.accounts[name].getevents(), key=lambda e: e.date):
                v.append(e.amount)
                d.append(e.date)
                
                b = e.amount
                try:
                    b += t[-1]
                except IndexError:
                    pass
                t.append(b)


            ax.step(d, t, where='post', label=name)
            ax.legend(shadow=True, loc = 'center left', bbox_to_anchor = (1.0, 0.5))
            ax.set_xlim([start, end])

        plt.show()

def main():
    s = Scenario('budget.csv')
    s.plot()
    #general = Account(name="General")


if __name__ == '__main__':
    sys.exit(main())
