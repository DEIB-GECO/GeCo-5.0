# NOT IMPLEMENTED YET
class ProjectMetadataLogic:
    def __init__(self, op):
        self.op = op
        self.op.executed = True
        self.result = self.op.depends_on.result

# NOT IMPLEMENTED YET
class ProjectRegionLogic:
    def __init__(self, op):
        self.op = op
        self.op.executed = True
        self.result = self.op.depends_on.result