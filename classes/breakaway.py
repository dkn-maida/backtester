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

        i=210
        while(i < len(self.bars)):

            o=self.bars.loc[i].open
            c=self.bars.loc[i].close
            pc=self.bars.loc[i-1].close

            if(self.longConditions(o, pc)):
                j=0
                res=0
                while(i+j < len(self.bars) and j < 7 and res <= 0):
                    res=self.longplay(self, o, c)
                    j=j+1
                    c=self.bars.loc[i+j].close
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