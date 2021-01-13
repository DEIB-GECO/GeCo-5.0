from workflow.workflow_class import UnaryOperation, BinaryOperation

class Scatter(BinaryOperation):
    def __init__(self, op1, op2):
        super().__init__(op1, op2)
        # joinby is a list of names of metadata
        #self.joinby = joinby