# NOT IMPLEMENTED YET
class JoinLogic:

    def __init__(self, op):
        self.op = op
        self.op.executed= True
        self.result = self.op.depends_on.result