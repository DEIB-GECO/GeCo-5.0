from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn import *
from logic.pivot_logic import PivotRes
from logic.kmeans_logic import ClusteringRes

class DBScanLogic:
    def __init__(self, dbscan):
        self.op = dbscan
        self.ds = self.op.depends_on.result
        if  isinstance(self.ds, PivotRes):
            self.labels = self.ds.labels
            self.ds = self.ds.ds
        self.tuning = dbscan.tuning
        if self.tuning:
            self.min_samp = dbscan.min_samp
            self.max_samp = dbscan.max_samp
            self.min_eps = dbscan.min_eps
            self.max_eps = dbscan.max_eps
        else:
            self.epsilon = dbscan.epsilon
            self.min_samples = dbscan.min_samples
        self.run()

    def run(self):
        if hasattr(self, 'labels'):
            for i in self.labels:
                if i in self.ds.columns:
                    self.ds = self.ds.drop(i, axis=1)
                elif i in self.ds.index:
                    self.ds = self.ds.drop(i, axis=0)

        if not self.tuning:
            dbscan = DBSCAN(eps=self.epsilon, min_samples=self.min_samples).fit(self.ds.values)
            label =  dbscan.labels_
            self.op.result = ClusteringRes(self.ds.values, dbscan, label)
        else:

            def silhouette_score(estimator, X):
                clusters = estimator.fit_predict(self.ds.values)
                #print(X)
                score = metrics.silhouette_score(self.ds.values, clusters)
                return score

            param_grid = {"eps": range(self.min_eps, self.max_eps), "min_samples":range(self.min_samp, self.max_samp) }
            # run randomized search
            search = GridSearchCV(DBSCAN(),
                                  param_grid=param_grid,
                                  scoring=silhouette_score)
            grid = search.fit(self.ds.values)
            dbscan = grid.best_estimator_
            dbscan_fit = dbscan.fit(self.ds.values)
            label = dbscan_fit.labels_
            self.op.result = ClusteringRes(self.ds.values, dbscan_fit, label)
        self.op.executed = True
        #self.write()

    def write(self):
        if not self.tuning:
            with open('jupyter_notebook.ipynb', 'a') as f:
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": [from sklearn.cluster import KMeans\n]},')
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": [kmeans = KMeans(n_clusters={})\n'.format(self.n_clust)+'kmeans_fit=kmeans.fit(table.values)\nlabels=kmeans.fit_predict(table.values)]},')
            f.close()

            with open('python_script.py', 'a') as f:
                f.write('from sklearn.cluster import KMeans\n'+
                        'kmeans = KMeans(n_clusters={})\nkmeans_fit=kmeans.fit(table.values)\nlabels=kmeans.fit_predict(table.values)'.format(self.n_clust))
            f.close()
        else:
            with open('jupyter_notebook.ipynb', 'a') as f:
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": ['+
                        'from sklearn.cluster import KMeans\n' +
                        'from sklearn.model_selection import GridSearchCV\n'+
                        'from sklearn import *\n'+
                        ']},')
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": ['+
                        'def silhouette_score(estimator, X):\n' +
                        '\tclusters = estimator.fit_predict(table.values)\n' +
                        '\tscore = metrics.silhouette_score(table.values, clusters)\n' +
                        '\treturn score\n\n'+
                        ']},')
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": [' +
                        'param_grid = {"n_clusters": range')
                f.write('({}, {})'.format(self.min, self.max)+'}\n')
                f.write('search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)\n'+
                        'grid = search.fit(table.values)\n'+'labels=search.fit_predict(table.values)\n'+
                        ']},')
            f.close()

            with open('python_script.py', 'a') as f:
                f.write('from sklearn.cluster import KMeans\n' +
                        'from sklearn.model_selection import GridSearchCV\n'+
                        'from sklearn import *\n'+
                        'def silhouette_score(estimator, X):\n'+
                        '\tclusters = estimator.fit_predict(table.values)\n'+
                        '\tscore = metrics.silhouette_score(table.values, clusters)\n'+
                        '\treturn score\n\n'+
                        'param_grid = {"n_clusters":'+ 'range({}, {})'.format(self.min, self.max)+'}\n'+
                        'search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)\n'+
                        'grid = search.fit(table.values)\n'+'labels=search.fit_predict(table.values)\n')
            f.close()




'''
optimizations:
- select only some regions
- order by optimization
'''