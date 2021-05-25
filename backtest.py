import sys
import statistics
from classes.extractor import Extractor
from classes.gapsetup import Gapsetup


def main():

    winrates=[]
    totalTrades = 0

    for security in sys.argv[1:]:

        #print('Starting  reading')
        extractor=Extractor()
        bars=extractor.read('data/'+ security +'.csv')
        taken=0
        wins = 0
        losses=0
        winrate=0.0
        
        previous=bars[0]
        for bar in bars[1:]:
            g=Gapsetup(previous, bar)
            if g.entryTrigger():
                taken+=1
                if(g.isWinner()):
                    wins+=1
                else:
                    losses+=1
            previous=bar
        
        # print("%d trades" % taken)
        # print("%d winners" % wins)
        # print("%d losses" % losses)
        if taken != 0:
            winrate=(wins/taken)*100
        # print("%f win rate" % winrate)
        winrates.append(winrate)
        totalTrades+=taken
    
    print('%d total trades' % totalTrades)
    globalwinrate = statistics.mean(winrates)
    print('global winrate is %f' % globalwinrate)
    

if __name__ == '__main__':
    main()