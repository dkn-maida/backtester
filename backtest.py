import sys
import pandas as pd
import matplotlib.pyplot as plt
from classes.gapsetup import Gapsetup
from classes.reversionsetup import ReversionSetup


def main():

    def reversion():
        for stk in sys.argv[2:]:
            print('starting reversion setup backtest')
            bars=pd.read_csv('data/daily/'+ stk +'.csv')
            r=ReversionSetup(bars, stk)
            r.backtest()
            print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(r.taken, r.wins, r.losses, r.winrate))
            print("average result is {:.2f} payoff is {:.2f}".format(r.averageres, r.payoff))
            df=pd.DataFrame(r.res)
            plt.hist(df, bins=[-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
            plt.show()

    def gap():
        for stk in sys.argv[2:]:

            bars=pd.read_csv('data/daily/'+ stk +'.csv')
            g=Gapsetup(bars, stk)
            g.backtest()
            print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(g.taken, g.wins, g.losses, g.winrate))
            print("average result is {:.2f} payoff is {:.2f}".format(g.averageres, g.payoff))
            df=pd.DataFrame(g.res)
            plt.hist(df, bins=[-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
            plt.show()

    if(sys.argv[1] == 'gap'):
        gap()
        
    if(sys.argv[1] == 'reversion'):
        reversion()
        
        
if __name__ == '__main__':
    main()