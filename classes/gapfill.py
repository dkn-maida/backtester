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
            pc=p.close
            pl=p.low
            ph=p.high
            if(self.entryConditions(o,pc,ph,pl)):
                res=self.gapplay(self.bars.loc[i], pc)/o*100
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

        if(self.taken > 0):
            self.winrate=(self.wins/self.taken)
            self.averageres=statistics.mean(self.res)
            if(len(self.winsr) > 0):
                self.avgw=statistics.mean(self.winsr)
            if(len(self.lossesr) > 0):
                self.avgl=statistics.mean(self.lossesr)
                self.payoff=self.avgw/self.avgl
       
    def isGapHaussier(self, o, pc) -> bool:
        return o < pc and o >= pc * 0.99 and o <= pc * 0.997
 
    def isGapBaissier(self, o, pc) -> bool:
        return o > pc and o <= pc * 1.01 and o >= pc * 1.003

    def inPreviousRange(self, o, ph, pl) -> bool:
        return o <= ph and o >= pl

    def entryConditions(self,o,pc,ph,pl)->bool:
        basic=(self.isGapHaussier(o, pc) or self.isGapBaissier(o, pc) and self.inPreviousRange(o, ph, pl))
        return basic
                    

    def isFilled(self, o, pc, h, l)->bool:
        if o > pc:
            return l <= pc
        if o < pc:
            return h >= pc

    def gapplay(self, bar, target):

        res=0
        date=int(bar.date)
        date=str(date)
        bars=None

        try:
            bars=pd.read_csv('data/5mins/'+ self.stk + '/' + date +'.csv')
            print('playing gap on %s' % date)
            i=0
            first=bars.loc[i]
            gapsize=abs(first.open-target)/first.open *100
            print('open is {} target is {} gapsize is {}'.format(first.open, target, gapsize))
        
            if(first.open > target):
             
            
                print('This is a gap Up')
                while(i < 70 and bars.loc[i].low > target):
                    i+=1
                if( bars.loc[i].low <= target):
                    res=first.open-target
                else:
                    res=first.open - bars.loc[i].close

            elif(first.open < target):
                print('This is a gap Down')
                while(i < 70 and bars.loc[i] < target):
                    i+=1
                if( bars.loc[i].high >= target ):
                    res=target - first.open 
                else:
                    res=bars.loc[i].close - first.open 

            print('res is {}'.format(res/first.open * 100)) 
            return res

        except:
            pass
        return res