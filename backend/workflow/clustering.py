from workflow.workflow_class import UnaryOperation

class KMeans(UnaryOperation):
    def __init__(self, op, clusters=None, tuning=False,  min=None, max=None):
        super().__init__(op)
        self.tuning = tuning
        if tuning==True:
            self.min_clusters = min
            self.max_clusters = max
        else:
            self.clusters = clusters

