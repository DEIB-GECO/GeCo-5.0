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

class DBScan(UnaryOperation):
    def __init__(self, op, epsilon=0.5, min_samples=5, tuning=False,  min_eps=None, max_eps=None, min_samp=None, max_samp=None):
        super().__init__(op)
        self.tuning = tuning
        if tuning==True:
            self.min_eps = min_eps
            self.max_eps = max_eps
            self.min_samp = min_samp
            self.max_samp = max_samp
        else:
            self.epsilon = epsilon
            self.min_samples = min_samples
