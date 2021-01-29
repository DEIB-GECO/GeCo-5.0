from workflow.workflow_class import UnaryOperation

class RandomForest(UnaryOperation):
    def __init__(self, op, crossval=True, estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1,
                 tuning=False,  min_est=None, max_est=None, n_est=1, min_md=None, max_md=None,n_md=1, min_mss=None, max_mss=None,n_mss=1, min_msl=None, max_msl=None, n_msl=1):
        super().__init__(op)
        self.crossval = crossval
        self.tuning = tuning
        if tuning==True:
            self.min_est = min_est
            self.max_est = max_est
            self.n_est = n_est
            self.min_md = min_md
            self.max_md = max_md
            self.n_md = n_md
            self.min_mss = min_mss
            self.max_mss = max_mss
            self.n_mss = n_mss
            self.min_msl = min_msl
            self.max_msl = max_msl
            self.n_msl = n_msl
        else:
            self.estimators = estimators
            self.max_depth = max_depth
            self.min_sample_leaf = min_samples_leaf
            self.min_sample_split = min_samples_split
