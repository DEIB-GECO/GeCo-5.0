class JoinPivotLogic:
    def __init__(self, op):
        self.op = op
        self.table_1 = self.op.depends_on.result.pivot
        self.table_2 = self.op.depends_on_2.result.pivot
        self.run()

    def run(self):
        print(self.table_1.head())
        print(self.table_2.head())
        if self.op.joinby!=None:
            res = self.table_1.join(self.table_2, on=self.op.joinby.name)
        else:
            res = self.table_1.join(self.table_2)
        print(res.head())
        self.op.executed = True
        self.op.result = res