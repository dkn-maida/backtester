
import pandas as pd
import statistics

class Gapsetup:

    def __init__(self, bars, stk):
        self.stk=stk
        self.bars=bars
        self.wins=0
        self.losses=0
        self.winrate=0.0
        self.taken=0
        self.winsr=[]
        self.lossesr=[]
        self.res=[]
        self.averageres=0.0
        self.avgw=0.0
        self.avgl=0.0
        self.payoff=0

    def backtest(self):
        p=(self.bars.loc[0])
        for i in range(1, len(self.bars)):
            o=self.bars.loc[i].open
            h=self.bars.loc[i].high
            l=self.bars.loc[i].low
            pc=p.close
            pl=p.low
            ph=p.high
            if(self.entryConditions(o,pc,ph,pl)):
                res=self.gapplay(self.bars.loc[i], pc)
                if(res!=0):
                    self.taken+=1
                    self.res.append(res)
                if(res > 0):
                    self.wins+=1
                    self.winsr.append(res)
                if(res < 0):
                    self.losses+=1
                    self.lossesr.append(-res)
            p=self.bars.loc[i]
        self.winrate=(self.wins/self.taken)
        self.averageres=statistics.mean(self.res)
        self.avgw=statistics.mean(self.winsr)
        self.avgl=statistics.mean(self.lossesr)
        self.payoff=self.avgw/self.avgl
       
    def isGapHaussier(self, o, pc) -> bool:
        return o < pc and o >= pc * 0.99

    def isGapBaissier(self, o, pc) -> bool:
        return o > pc and o <= pc * 1.01

    def inPreviousRange(self, o, ph, pl) -> bool:
        return o <= ph and o >= pl

    def entryConditions(self,o,pc,ph,pl)->bool:
        return (self.isGapHaussier(o, pc) or self.isGapBaissier(o, pc)) and self.inPreviousRange(o, ph, pl)

    def isFilled(self, o, pc, h, l)->bool:
        if o > pc:
            return l <= pc
        if o < pc:
            return h >= pc

    def gapplay(self, bar, target, stopratio=20):

        res=0
        date=int(bar.date)
        date=str(date)
        bars=None

        try:
            bars=pd.read_csv('data/5mins/'+ self.stk + '/' + date +'.csv')
            print('playing gap on %s' % date)
            i=0
            firsthour=bars.loc[i]
            gapsize=abs(firsthour.open-target)
            print('open is {} target is {} gapsize is {}'.format(firsthour.open, target, gapsize))
            df=pd.DataFrame(bars)
        
            #gap baissier
            if(firsthour.open > target):
                print('This is a gap Up')
                stop = firsthour.open + gapsize * stopratio
                print('Stop is %f' % stop)
                while(i < 18 and firsthour.high < stop and firsthour.low > target):
                    i+=1
                    firsthour=bars.loc[i]
                if(firsthour.high >= stop):
                    res=-stopratio * gapsize
                elif( firsthour.low <= target ):
                    res=firsthour.open-target
                else:
                    res=firsthour.open-firsthour.close

            #gap haussier
            elif(firsthour.open < target):
                print('This is a gap Down')
                stop = firsthour.open - gapsize * stopratio
                print('Stop is %f' % stop)
                while(i < 18 and firsthour.low > stop and firsthour.high < target):
                    i+=1
                    firsthour=bars.loc[i]
                if(firsthour.low <= stop):
                    res=-stopratio * gapsize
                elif( firsthour.high >= target ):
                    res=target-firsthour.open
                else:
                    res=firsthour.close-firsthour.open

            print('res is %f' % res)
            return res

        except:
            pass
        return res