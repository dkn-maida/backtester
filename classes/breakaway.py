from ta.trend import SMAIndicator


class BreakAwaySetup:

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

        print('backtest')

        # Initialize SMA Indicator
        sma50=SMAIndicator(close=self.bars["close"], window=50)
        sma100=SMAIndicator(close=self.bars["close"], window=100)
        sma200=SMAIndicator(close=self.bars["close"], window=200)

        self.bars['sma50'] = sma50.sma_indicator()
        self.bars['sma100'] = sma100.sma_indicator()
        self.bars['sma200'] = sma200.sma_indicator()

        i=214
        res=0
        while(i < len(self.bars)):

            o=self.bars.loc[i].open
            c=self.bars.loc[i].close
            pc=self.bars.loc[i-1].close
            sma50=self.bars.loc[i].sma50
            sma100=self.bars.loc[i].sma100
            sma200=self.bars.loc[i].sma200

            print("On {} sma50 {}, 100 {} and 200 {}".format(self.bars.loc[i].date, sma50, sma100, sma200))
            print("Open is {} previous close is {}".format(o,pc))

            if(self.longConditions(o, pc, sma50, sma100, sma200)):
                print("Long trade taken on {}".format(self.bars.loc[i].date))
                j=0
                res=0
                self.taken += 1
                while(i+j < len(self.bars) and j < 7 and res < 0):
                    res=self.longplay(self, o, c)
                    j=j+1
                    c=self.bars.loc[i+j].close

            if(self.shortConditions(o, pc, sma50, sma100, sma200)):
                print("Short trade taken on {}".format(self.bars.loc[i].date))
                j=0
                res=0
                self.taken += 1
                while(i+j < len(self.bars) and j < 7 and res < 0):
                    res=self.shortplay(self, o, c)
                    j=j+1
                    c=self.bars.loc[i+j].close
                print('res is {}'.format(res))
            
            if res > 0:
                self.wins+=1
                self.winsr.append(res)
                self.res.append(res)
            if res < 0:
                self.losses+=1
                self.lossesr.append(-res)
                self.res.append(res)
            i=i+7




    def longConditions(self, o, pc, sma50, sma100, sma200) -> bool:
        longCondition = (o > sma50 and pc < sma50) or (o > sma100 and pc < sma100) or (o > sma200 and pc < sma200)
        return longCondition

    def shortConditions(self, o, pc, sma50, sma100, sma200) -> bool:
        shortCondition = (o < sma50 and pc > sma50) or (o < sma100 and pc > sma100) or (o < sma200 and pc > sma200)
        return shortCondition

    def longplay(self,o,c):
        return (c-o)/o*100

    def shortplay(self,o,c):
        return (o-c)/o*100