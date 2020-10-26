#from data_structure.context import Operation
from workflow import *
#from workflow.workflow_class import UnaryOperation, BinaryOperation, Workflow
class Pivot(UnaryOperation):
    def __init__(self, op, region_row, metadata_column, region_value):
        super().__init__(op)
        self.row = region_row
        self.column = metadata_column
        self.value = region_value

class JoinPivot(BinaryOperation):
    def __init__(self, op, op2):
        super().__init__(op, op2)

class ConcatenatePivot(BinaryOperation):
    def __init__(self, op, op2):
        super().__init__(op, op2)

