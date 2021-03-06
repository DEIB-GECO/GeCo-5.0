class ProjectRegionLogic:
    def __init__(self, select):
        self.op = select
        self.ds = self.op.depends_on
        self.run()

    def run(self):
        self.op.executed = True
        self.op.result = self.op.depends_on

