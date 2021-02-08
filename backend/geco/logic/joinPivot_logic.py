class JoinPivotLogic:
    def __init__(self, op):
        self.op = op
        self.table_1 = self.op.depends_on.result
        self.table_2 = self.op.depends_on_2.result
        self.run()

    def run(self):
        if self.op.joinby!=None:
            res = self.table_1.join(self.table_2, on=self.op.joinby.name)
        else:
            res = self.table_1.join(self.table_2)

        self.op.executed = True
        self.op.result = res