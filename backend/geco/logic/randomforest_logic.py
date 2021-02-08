from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np

class RandomForestLogic:
    def __init__(self, rf):
        self.op = rf
        self.ds = self.op.depends_on.result
        self.tuning = rf.tuning
        self.crossval = rf.crossval
        if self.tuning:
            self.min_est = rf.min_est
            self.max_est = rf.max_est
            self.n_est = rf.n_est
            self.min_md = rf.min_md
            self.max_md = rf.max_md
            self.n_md = rf.n_md
            self.min_mss = rf.min_mss
            self.max_mss = rf.max_mss
            self.n_mss = rf.n_mss
            self.min_msl = rf.min_msl
            self.max_msl = rf.max_msl
            self.n_msl = rf.n_msl
        else:
            self.estimators = rf.estimators
            self.max_depth = rf.max_depth
            self.min_sample_leaf = rf.min_samples_leaf
            self.min_sample_split = rf.min_samples_split
        self.run()

    def run(self):

        if self.crossval:
            if self.tuning:
                rf = RandomForestClassifier()
                # Number of trees in random forest
                n_estimators = [int(x) for x in np.linspace(start=self.min_est, stop=self.max_est, num=self.n_est)]
                # Maximum number of levels in tree
                max_depth = [int(x) for x in np.linspace(self.min_md, self.max_md, num=self.n_md)]
                max_depth.append(None)
                # Minimum number of samples required to split a node
                min_samples_split = [int(x) for x in np.linspace(self.min_mss, self.max_mss, num=self.n_mss)]
                # Minimum number of samples required at each leaf node
                min_samples_leaf = [int(x) for x in np.linspace(self.min_msl, self.max_msl, num=self.n_msl)]

                # Create the random grid
                param_grid = {'n_estimators': n_estimators,
                               'max_depth': max_depth,
                               'min_samples_split': min_samples_split,
                               'min_samples_leaf': min_samples_leaf}

                # Instantiate the grid search model
                grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
                                           cv=3, n_jobs=-1, verbose=2)
                grid_search.fit(self.ds, self.ds.labels)
            else:
                rf = RandomForestClassifier(n_estimators=self.estimators, max_depth=self.max_depth, min_samples_split=self.min_sample_split, min_samples_leaf=self.min_sample_leaf)
                fit = rf.fit(self.ds, self.ds.labels)
