class ConcatenatePivot:
    def __init__(self, op):
        self.op = op
        self.table_1 = self.op.depends_on.result
        self.table_2 = self.op.depends_on_2.result
        self.run()

    def run(self):
        res = self.table_1.append(self.table_2)

        self.op.executed = True
        self.op.result = res