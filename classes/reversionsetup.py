from numpy import longcomplex
from classes.bar import Bar
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta import add_all_ta_features
import statistics

class ReversionSetup:

    def __init__(self, bars, stk):
        self.bars=bars
        self.stk=stk
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
        self.jumper=0

    def backtest(self):

        print('backtest')
        # Initialize Bollinger Bands Indicator
        bb = BollingerBands(close=self.bars["close"], window=10, window_dev=1.5) 
        self.bars['bbh'] = bb.bollinger_hband()
        self.bars['bbl'] = bb.bollinger_lband()

        p=(self.bars.loc[10])
        for i in range(11, len(self.bars)):
            
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
                res=self.longplay(o,c,h)
                
                if(res > 0):
                    res=(res/o)*100
                    self.wins+=1
                    self.winsr.append(res)
                    self.res.append(res)
                    print('Long on {} res is {}'.format(self.bars.loc[i].date, res))
                else:
                    j=1
                    while(j<7 and res < o * 0.03):
                        c=self.bars.loc[i+j].close
                        h=self.bars.loc[i+j].high
                        res=self.longplay(o,c,h)
                        j+=1
                    print('res after {} days is {}'.format(j,res))
                    self.jumper=j
                    self.res.append(res)
                    if(res > 0):
                        res=(res/o)*100
                        self.wins+=1
                        self.winsr.append(res)
                    else:
                        res=(res/o)*100
                        self.losses+=1
                        self.lossesr.append(-res)
                    print('Long on {} res is {} after {} days'.format(self.bars.loc[i].date, res,j))
               
            if(self.shortConditions(po,pc,o,bbh)):
                self.taken+=1
                res=self.shortplay(o,c,l)
                
                if(res < 0):
                    self.wins+=1
                    res=(res/o)*100
                    self.winsr.append(res)
                    self.res.append(res)
                    print('Short on {} res is {}'.format(self.bars.loc[i].date, res))
                else:
                    j=1
                    while(j<7 and res < o * 0.03):
                        c=self.bars.loc[i+j].close
                        l=self.bars.loc[i+j].low
                        res=self.shortplay(o,c,l)
                        j+=1
                    print('res after {} days is {}'.format(j,res))
                    self.jumper=j
                    self.res.append(res)

                    if(res > 0):
                        self.wins+=1
                        res=(res/o)*100
                        self.winsr.append(res)
                    else:
                        self.losses+=1
                        res=(res/o)*100
                        self.lossesr.append(-res)

                    print('Short on {} res is {} after {} days'.format(self.bars.loc[i].date, res,j))


            # print('jumper is {}'.format(self.jumper))
            p=(self.bars.loc[i+self.jumper])
            
        self.winrate=(self.wins/self.taken)
        self.averageres=statistics.mean(self.res)
        self.avgw=statistics.mean(self.winsr)
        self.avgl=statistics.mean(self.lossesr)
        self.payoff=self.avgw/self.avgl

    def longConditions(self, po, pc, o, bbl) -> bool:
        longCondition = po > bbl and pc < bbl and o < bbl
        return longCondition

    def shortConditions(self, po, pc, o, bbh) -> bool:
        shortCondition = po < bbh and pc > bbh and o > bbh
        return shortCondition

    def longplay(self,o,c,h):
        if h-o >= o*0.03:
            return h-o 
        return c-o

    def shortplay(self,o,c,l):
        if o-l >= o*0.03:
            return o-l 
        return o-c

   
