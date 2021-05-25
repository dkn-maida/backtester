from classes.bar import Bar

class Gapsetup:

    def __init__(self, previous: Bar, current: Bar):
        self.open=current.open
        self.high=current.high
        self.low=current.low
        self.pclose=previous.close
        self.phigh=previous.high
        self.plow=previous.low 

    def isGapHaussier(self) -> bool:
        return self.open < self.pclose and self.open >= self.pclose * 0.995

    def isGapBaissier(self) -> bool:
        return self.open > self.pclose and self.open <= self.pclose * 1.005

    def isInteresting(self) -> bool:
        return abs(self.open-self.pclose) >= 0.25

    def inPreviousRange(self) -> bool:
        return self.open <= self.phigh and self.open >= self.plow

    def entryTrigger(self)->bool:
        return (self.isGapHaussier() or self.isGapBaissier()) \
        and self.isInteresting() and self.inPreviousRange()

    def isWinner(self)->bool:
        stop=0
        if self.open > self.pclose:
            return self.low <= self.pclose
        if self.open < self.pclose:
            return self.high >= self.pclose
        
    @property
    def gapsize(self) ->float:
        return abs(self.open-self.pclose)
            