from enum import Enum
class Aggregate(Enum):
    COUNT = 0
    BAG = 1
    BAGD = 2
    AVG = 3
    MIN = 4
    MAX = 5
    MEDIAN = 6
    STD = 7

    def switch(self, msg):
        if msg.lower() in ['bag', 'bagging']:
            return self.BAG
        elif msg.lower() in ['bagd', 'bag distinct']:
            return self.BAGD
        elif msg.lower() in ['avg', 'mean', 'average']:
            return self.AVG
        elif msg.lower() in ['min', 'minimum']:
            return self.MIN
        elif msg.lower() in ['max', 'maximum']:
            return self.MAX
        elif msg.lower() in ['median']:
            return self.MEDIAN
        elif msg.lower() in ['std', 'standard dev', 'dev']:
            return self.STD
        else:
            return None


