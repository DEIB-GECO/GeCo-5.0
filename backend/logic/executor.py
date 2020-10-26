class ExecutorLogic:
    def __init__(self, workflow):
        self.workflow = workflow

    def run(self):
        gmql_operation = ['Select', 'ProjectMetadata', 'ProjectRegion', 'Cover', 'Join', 'Union', 'Map', 'Difference']
        pivot_operation = ['Pivot', 'JoinPivot', 'ConcatenatePivot']
        gmql_ops = []
        pivot_ops = []
        for i in range(len(self.workflow), 0):
            elem = self.workflow[i]
            if elem.executed==True:
                break
            elif elem.__class__.__name__ in gmql_operation:
                gmql_ops.append(elem)
            elif elem.__class__.__name__ in pivot_operation:
                pivot_ops.append(elem)
        if gmql_ops!=[]:
            GMQL_Logic(self.workflow, gmql_ops)
        if pivot_ops!=[]:
            Pivot_Logic(self.workflow, pivot_ops)


#TOMMASO
class GMQL_Logic:
    pass

class Pivot_Logic:
    pass




