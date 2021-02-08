from workflow.workflow_class import UnaryOperation

class PCA(UnaryOperation):
    def __init__(self, op, components=2):
        super().__init__(op)
        self.components = components
