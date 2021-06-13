from ta.volatility import BollingerBands
import statistics
import pandas as pd

class ReversionSetup:

    def __init__(self, bars, stk, start_date='20010101'):

        self.bars=bars
        self.stk=stk
        self.wins=0
        self.losses=0
        self.winrate=0.0
        self.taken=0
        self.winsr=[]
        self.lossesr=[]
        self.res=[]
        self.duration=[]
        self.averageres=0.0
        self.avgduration=0.0
        self.avgw=0.0
        self.avgl=0.0
        self.payoff=0
        self.jumper=0
        self.durationlimit=20
        self.stop=10
        self.start_date=start_date
        
    def backtest(self):

        print('backtest')
        
        # Initialize Bollinger Bands Indicator
        bb = BollingerBands(close=self.bars["close"], window=10, window_dev=1.5) 
        self.bars['bbh'] = bb.bollinger_hband()
        self.bars['bbl'] = bb.bollinger_lband()

        self.start_date = pd.to_datetime( self.start_date, format='%Y%m%d') 
        self.bars['date'] = pd.to_datetime( self.bars['date'], format='%Y%m%d') 
        p=(self.bars.loc[10])
        i=11
        while(i < len(self.bars) and self.bars.loc[i].date < self.start_date):
            i=i+1
        
       
        while (i < len(self.bars)):
            
            o=self.bars.loc[i].open
            c=self.bars.loc[i].close
            l=self.bars.loc[i].low
            h=self.bars.loc[i].high
            po=p.open
            pc=p.close
            bbl=self.bars.loc[i-1].bbl
            bbh=self.bars.loc[i-1].bbh
            self.jumper=0

            if(self.longConditions(po,pc,o,bbl)):

                self.taken+=1
                res=self.longplay(o,c,h,l)
                print('Open is {} at {} bbl is {} res of first day is {}'.format(o, self.bars.loc[i].date, bbl, res))

                j=1
                while( res < 0 and res > -self.stop  and j < self.durationlimit and i+j < len(self.bars.index)):
                    c=self.bars.loc[i+j].close
                    h=self.bars.loc[i+j].high
                    l=self.bars.loc[i+j].low
                    res=self.longplay(o,c,h,l)
                    j+=1
                self.jumper=j
               
                if(res > 0):
                    self.wins+=1
                    self.winsr.append(res)
                    self.res.append(res)
                else:
                    self.losses+=1
                    self.lossesr.append(-res)
                    self.res.append(res)

                self.duration.append(j)
                print('Long on {} at {} res is {} after {} days'.format(self.stk,self.bars.loc[i].date, res,j))
               
            if(self.shortConditions(po,pc,o,bbh)):

                self.taken+=1
                res=self.shortplay(o,c,l,h)
                print('Open is {} at {} bbh is {} res of first day is {}'.format(o, self.bars.loc[i].date, bbh, res))
                
                j=1
                while( res < 0 and res > -self.stop and j < self.durationlimit and i+j < len(self.bars.index) ):

                    c=self.bars.loc[i+j].close
                    l=self.bars.loc[i+j].low
                    h=self.bars.loc[i+j].high
                    res=self.shortplay(o,c,l,h)
                    j+=1  
                self.jumper=j
              
                if(res > 0):
                    self.wins+=1
                    self.winsr.append(res)
                    self.res.append(res)
                else:
                    self.losses+=1
                    self.lossesr.append(-res)
                    self.res.append(res)

                self.duration.append(j)
                print('Short on {} at {} res is {} after {} days'.format(self.stk, self.bars.loc[i].date, res,j))

            if(i + self.jumper + 1 < len(self.bars)):
                p=(self.bars.loc[ i + self.jumper])
                i+=(self.jumper + 1)
            else:
                i+=1
                break

        if(self.taken > 0):
            if (self.wins > 0 ):
                self.winrate=(self.wins/self.taken)
            if(self.losses > 0 and self.wins > 0):
                self.avgl=statistics.mean(self.lossesr)
                self.avgw=statistics.mean(self.winsr)
                self.payoff=self.avgw/self.avgl
            self.averageres=statistics.mean(self.res)
            self.avgduration=statistics.mean(self.duration)

    def longConditions(self, po, pc, o, bbl) -> bool:
        longCondition = po > bbl and pc < bbl and o < bbl
        return longCondition

    def shortConditions(self, po, pc, o, bbh) -> bool:
        shortCondition = po < bbh and pc > bbh and o > bbh
        return shortCondition

    def longplay(self,o,c,h,l):
        if l <= o * 0.9:
            return -10
        if h >= o * 1.1:
            return 10
        return (c-o)/o*100

    def shortplay(self,o,c,l,h):
        if h >= o * 1.1:
            return -10
        if l <= o * 0.9:
            return 10
        return (o-c)/o*100 