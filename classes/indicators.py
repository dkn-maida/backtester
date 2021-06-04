class Indicators:

    def __init__(self):
        pass

    def pivots(self,h,l,c):

        pp = ( h + l + c)/3 
        r4 = pp + (h-l) * 3
        r3 = pp + (h-l) * 2
        r2 = pp + (h-l)
        r1 = 2 * pp - l
        s1 = 2 * pp - h
        s2 = pp - (h-l)
        s3 = pp - (h-l) * 2
        s4 = pp - (h-l) * 3
        
        return {
            'r4': r4,
            'r3': r3,
            'r2': r2,
            'r1': r1,
            'pp': pp,
            's1': s1,
            's2': s2,
            's3': s3,
            's4': s4
        }