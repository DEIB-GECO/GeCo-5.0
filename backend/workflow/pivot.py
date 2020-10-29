#from data_structure.context import Operation
from workflow import *
#from workflow.workflow_class import UnaryOperation, BinaryOperation, Workflow
class Pivot(UnaryOperation):
    def __init__(self, op, region_row=None, region_column= None, metadata_row= None, metadata_column= None, region_value= None):
        super().__init__(op)
        self.region_row = region_row
        self.meta_row = metadata_row
        self.region_col = region_column
        self.meta_col = metadata_column
        self.value = region_value

class JoinPivot(BinaryOperation):
    def __init__(self, op, op2):
        super().__init__(op, op2)

class ConcatenatePivot(BinaryOperation):
    def __init__(self, op, op2):
        super().__init__(op, op2)

