import statistics
import sys
import pandas as pd
from classes.gapfill import Gapsetup 
from classes.reversion import ReversionSetup
from classes.breakaway import BreakAwaySetup

global_res=[]
global_taken=0
global_wins=0 
global_losses=0
global_winrate=0.0
global_taken=0
global_winsr=[]
global_lossesr=[]
global_res=[]
global_averageres=0.0
global_avgw=0.0
global_avgl=0.0
global_payoff=0.0
global_avgduration=[]

def main():

    def reversion():
        start_date=sys.argv[2]
        global global_res, global_lossesr, global_winsr, global_avgduration
        for stk in sys.argv[3:]:
            print('starting reversion setup backtest')
            bars=pd.read_csv('data/daily/'+ stk +'.csv')
            r=ReversionSetup(bars, stk, start_date)
            r.backtest()
            # print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(r.taken, r.wins, r.losses, r.winrate))
            # print("average result is {:.2f} payoff is {:.2f}".format(r.averageres, r.payoff))
            # df=pd.DataFrame(r.res)
            # plt.hist(df, bins=[-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
            # plt.show()
            if (r.taken > 0):
                global_res = global_res + r.res
                global_winsr = global_winsr + r.winsr
                global_lossesr = global_lossesr + r.lossesr
                global_avgduration = global_avgduration + r.duration
                print('Global average duration is {}'.format(statistics.mean(global_avgduration)))

    def gap():
        global global_res, global_lossesr, global_winsr
        for stk in sys.argv[2:]:
            bars=pd.read_csv('data/daily/'+ stk +'.csv')
            g=Gapsetup(bars, stk)
            g.backtest()
            # print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(g.taken, g.wins, g.losses, g.winrate))
            # print("average result is {:.2f} payoff is {:.2f}".format(g.averageres, g.payoff))
            # df=pd.DataFrame(g.res)
            # plt.hist(df, bins=[-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
            # plt.show()
            global_res = global_res + g.res
            global_winsr = global_winsr + g.winsr
            global_lossesr = global_lossesr + g.lossesr

    def breakaway():
        global global_res, global_lossesr, global_winsr
        for stk in sys.argv[2:]:
            bars=pd.read_csv('data/hourly/'+ stk +'/'+ stk + '.csv')
            b=BreakAwaySetup(bars, stk)
            b.backtest()
            # print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(g.taken, g.wins, g.losses, g.winrate))
            # print("average result is {:.2f} payoff is {:.2f}".format(g.averageres, g.payoff))
            # df=pd.DataFrame(g.res)
            # plt.hist(df, bins=[-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
            # plt.show()
            global_res = global_res + b.res
            global_winsr = global_winsr + b.winsr
            global_lossesr = global_lossesr + b.lossesr


    if(sys.argv[1] == 'gap'): 
        gap()
    if(sys.argv[1] == 'reversion'):
        reversion()
    if(sys.argv[1] == 'breakaway'):
        breakaway()
    

    global_wins=len(global_winsr)
    global_losses=len(global_lossesr)
    global_taken=global_losses + global_wins
    global global_payoff, global_averageres, global_winrate

    if(global_taken > 0):
        global_winrate=(global_wins/global_taken)*100
        global_averageres=statistics.mean(global_res)
        if(len(global_winsr) > 0 and len(global_lossesr) > 0 and statistics.mean(global_lossesr) > 0):
            global_payoff=statistics.mean(global_winsr)/statistics.mean(global_lossesr)

    # print(global_res) 
    print("{} trades taken on total, {} wins, {} losses {:.2f}% winrate".format(global_taken ,global_wins, global_losses, global_winrate))
    print("Global average result is {:.2f} payoff is {:.2f}".format(global_averageres, global_payoff))
        
if __name__ == '__main__':
    main()