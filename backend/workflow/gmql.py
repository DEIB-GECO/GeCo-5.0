from workflow.workflow_class import UnaryOperation, BinaryOperation
from aggregates import Aggregate

class Select(UnaryOperation):
    pass

class ProjectMetadata(UnaryOperation):
    def __init__(self, op, change_dict=None, keep_list=None):
        super().__init__(op)
        self.change = change_dict
        self.keep = keep_list

class ProjectRegion(UnaryOperation):
    def __init__(self, op, change_dict=None, keep_list=None):
        super().__init__(op)
        self.change = change_dict
        self.keep = keep_list

class Cover(UnaryOperation):
    def __init__(self, op, groupby=None, aggregate=Aggregate.COUNT, name_agg=None):
        super().__init__(op)
        self.groupby = groupby
        self.aggregate = aggregate
        self.name_agg = name_agg

class Union(BinaryOperation):
    pass

class Difference(BinaryOperation):
    pass

class Join(BinaryOperation):
    def __init__(self, op1, op2, joinby=None):
        super().__init__(op1, op2)
        self.joinby = joinby

class Map(BinaryOperation):
    def __init__(self, op1, op2, joinby=None, aggregate=Aggregate.COUNT, name_agg=None):
        super().__init__(op1, op2)
        self.joinby = joinby
        self.aggregate = aggregate
        self.name_agg = name_agg

