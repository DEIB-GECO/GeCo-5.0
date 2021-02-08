from workflow.workflow_class import UnaryOperation, BinaryOperation
#from data_structure.aggregates import Aggregate
#from data_structure.dataset import Field

class Select(UnaryOperation):
    def __init__(self, op, metadata: dict = None, region: dict = None):
        super().__init__(op)
        # dictionary with as keys the metadata name to filter, as value either a list of values or a logical operator
        self.metadata = metadata
        # dictionary with as keys the region name to filter, as value either a list of values or a logical operator
        self.region = region

class ProjectMetadata(UnaryOperation):
    def __init__(self, op, change_dict=None, keep_list: list=None):
        super().__init__(op)
        #dictionary with as keys the new metadata name, as value an aritmetic operation
        self.change = change_dict
        #list of metadata to keep
        self.keep = keep_list

class ProjectRegion(UnaryOperation):
    def __init__(self, op, change_dict=None, keep_list: list=None):
        super().__init__(op)
        # dictionary with as keys the new region name, as value an aritmetic operation
        self.change = change_dict
        # list of region data to keep
        self.keep = keep_list
'''
class Cover(UnaryOperation):
    def __init__(self, op, min='ANY', max='ANY' ,groupby: Field=None, aggregate=Aggregate.COUNT, name_agg=None):
        super().__init__(op)
        self.min = min
        self.max = max
        self.groupby = groupby
        self.aggregate = aggregate
       self.name_agg = name_agg
'''

class Union(BinaryOperation):
    pass

class Difference(BinaryOperation):
    pass

'''
class Join(BinaryOperation):
    def __init__(self, op1, op2, joinby: Field=None):
        super().__init__(op1, op2)
        # joinby is a list of names of metadata
        self.joinby = joinby

class Map(BinaryOperation):
    def __init__(self, op1, op2, joinby: Field=None, aggregate=Aggregate.COUNT, name_agg=None):
        super().__init__(op1, op2)
        # joinby is a list of names of metadata
        self.joinby = joinby
        self.aggregate = aggregate
        self.name_agg = name_agg

'''