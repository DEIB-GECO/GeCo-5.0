
class PivotLogic:
    def __init__(self, workflow):
        self.workflow = workflow

    def run(self):
        pivot_operation = ['Pivot', 'JoinPivot', 'ConcatenatePivot']
        for o in self.workflow:
            if o.__class__.__name__ in pivot_operation:
                fun = o.__class__.__name__.lower()
                res = getattr(self, fun)()
                o.result = res
                o.executed = True

    def pivot(self):
        pass
