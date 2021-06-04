import pandas as pd
import statistics

class Gapandgo:

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
            date=self.bars.loc[i].date

            if(self.longconditions(o, p.close, date)):

                res=self.longplay(self.bars.loc[i])

                if(res!=0):
                    self.taken+=1
                    self.res.append(res)

                if(res > 0):
                    self.wins+=1
                    self.winsr.append(res)

                if(res < 0):
                    self.losses+=1
                    self.lossesr.append(-res)


            # if(self.shortconditions(o,c)):
            #     res=self.shortplay(self.bars.loc[i])
            #     if(res!=0):
            #         self.taken+=1
            #         self.res.append(res)
            #     if(res > 0):
            #         self.wins+=1
            #         self.winsr.append(res)
            #     if(res < 0):
            #         self.losses+=1
            #         self.lossesr.append(-res)

            p=self.bars.loc[i]

        
        if(self.taken > 0):
            self.winrate=(self.wins/self.taken)
            self.averageres=statistics.mean(self.res)
            if(len(self.winsr) > 0):
                self.avgw=statistics.mean(self.winsr)
            if(len(self.lossesr) > 0):
                self.avgl=statistics.mean(self.lossesr)
                self.payoff=self.avgw/self.avgl
       
    def longconditions(self, o, pc, date) -> bool:
        if(o >= 10 and o >= pc * 1.05):
            gap=(o-pc)/pc*100
            print('On {} open is {} and pc is {} gap is {:.2f}%'.format(date, o, pc, gap))
            return True
 
    def shortconditions(self, o, pc) -> bool:
        return o <= pc * 0.95


    def longplay(self, bar):

        res=0
        date=int(bar.date)
        date=str(date)

        print('Playing Long gap and go on {} at {}'.format(self.stk, date))

        try:
            bars=pd.read_csv('data/5mins/'+ self.stk + '/' + date +'.csv')
            i=0
            current=bars.loc[i]
            entry=-1

            if(current.open-current.close > 0):
                entry=current.close
                print('First candle is downm entry is {}'.format(entry))

            else:
                while( i < len(bars.loc[i]-1) and current.close - current.open > 0):
                    i+=1
                    current=bars.loc[i]
                if( i == len(bars.loc[i])-1):
                    res=0
                    print('Long gap and go on {} at {} no entry res is {}'.format(self.stk, date, entry, res))
                    return res
                entry=current.close
            i+=1
            print('Entry is {} at candle {}'.format(entry, i))
            current=bars.loc[i]

            while(res < 3 and res > -3 and i < len(bars.loc[i])):
                if(current.high >= entry * 1.03):
                    res = 3
                if(current.low <= entry * 0.97):
                    res = -3
                i+=1
                current=bars.loc[i]
            if(i != -3 and i != 3):
                res=(bars.loc[77].close-entry)/entry * 100
            print('Long gap and go on {} at {} entry is {} res is {}'.format(self.stk, date, entry, res))
            
        except:
            print('no data')
            pass
        return res       
            

           

  