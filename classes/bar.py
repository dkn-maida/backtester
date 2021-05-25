class Bar:

    def __init__(self, date, open: float, high: float, low: float, close: float) -> None:
        self.date=date
        self.open=open
        self.high=high
        self.low=low
        self.close=close

    def __str__(self) -> str:
        return "date:" + self.date + "\n"\
        + 'open:' + str(self.open) + "\n"\
        + 'high:' + str(self.high) + "\n" \
        + 'low:' + str(self.low) + "\n" \
        + 'close:' + str(self.close) + "\n" 

    def dir(self) -> int:
        if self.close <= self.open*0.99:
            return -1
        if self.close >= self.open*1.01:
            return 1
        return 0

    @property
    def range(self) -> float:
        return abs(self.high-self.low)