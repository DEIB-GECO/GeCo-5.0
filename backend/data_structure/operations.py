from enum import Enum
from data_structure.dataset import Field

class ArithmeticOperation(Enum):
    SUM = 1
    SUBTRACT = 2
    PRODUCT = 3
    DIVISION = 4

    def parameters(self, op1=None, op2=None):
        if isinstance(op1,Field) or isinstance(op1,float) or isinstance(op1, ArithmeticOperation) or (op1==None):
            self.op1 = op1
        else:
            raise TypeError("Operator 1 has wrong type.")
        if isinstance(op2,Field) or isinstance(op2,float) or isinstance(op2, ArithmeticOperation) or (op2==None):
            self.op2 = op2
        else:
            raise TypeError("Operator 2 has wrong type.")
        return self


class LogicalOperation(Enum):
    LESSTHAN = 11
    MORETHAN = 12
    LESSEQUAL = 13
    MOREEQUAL = 14
    EQUAL = 15

    def parameter(self, op = None):
        if isinstance(op,float) or (op==None):
            self.op = op
        else:
            raise TypeError("Value has wrong type.")

        return self