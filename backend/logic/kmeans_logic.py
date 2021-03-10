from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn import *
import time
from logic.pivot_logic import PivotRes

class ClusteringRes:
    def __init__(self, name, values, kmeans_fit, labels):
        self.name = name
        self.values = values
        self.kmeans_fit = kmeans_fit
        self.labels = labels


class KMeansLogic:
    def __init__(self, kmeans, sid):
        self.op = kmeans
        self.ds = self.op.depends_on.result
        if  isinstance(self.ds, PivotRes):
            self.labels = self.ds.labels
            self.name = self.ds.name
            self.ds = self.ds.ds
        self.tuning = kmeans.tuning
        if self.tuning:
            self.min = kmeans.min_clusters
            self.max = kmeans.max_clusters
        else:
            self.n_clust = kmeans.clusters
        self.run(sid)

    def run(self, sid):
        pre = time.time()
        print('time pre', pre)
        if hasattr(self, 'labels'):
            for i in self.labels:
                if i in self.ds.columns:
                    self.ds = self.ds.drop(i, axis=1)
                elif i in self.ds.index:
                    self.ds = self.ds.drop(i, axis=0)
        print('tuning', self.tuning)

        if not self.tuning:
            print('n_clust',self.n_clust)
            kmeans = KMeans(n_clusters=self.n_clust)
            kmeans_fit = kmeans.fit(self.ds.values)
            labels =  kmeans.fit_predict(self.ds.values)
        else:
            print('min', self.min)
            print('max', self.max)

            def silhouette_score(estimator, X):
                clusters = estimator.fit_predict(self.ds.values)
                score = metrics.silhouette_score(self.ds.values, clusters)
                return score

            param_grid = {"n_clusters": range(self.min, self.max)}
            print('param_grid', param_grid)
            search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)
            grid = search.fit(self.ds.values)
            kmeans = grid.best_estimator_
            kmeans_fit = kmeans.fit(self.ds.values)
            labels = kmeans.fit_predict(self.ds.values)
        print('time post km', time.time()-pre)
        self.op.result = ClusteringRes(self.name, self.ds.values, kmeans_fit, labels)
        self.op.executed = True
       # self.write_script(sid, text)

    def write_script(self, sid, text):
        with open(f'python_script_{sid}.py', 'a') as f:
            f.write(text)

    def write(self,sid):

        if not self.tuning:
            with open(f'jupyter_notebook_{sid}.ipynb', 'a') as f:
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": [from sklearn.cluster import KMeans\n]},')
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        f'"source": [kmeans = KMeans(n_clusters={self.n_clust})\n'+
                        f'kmeans_fit=kmeans.fit({self.name}.values)\nlabels=kmeans.fit_predict({self.name}.values)]'+'},')

            with open(f'python_script_{sid}.py', 'a') as f:
                f.write('from sklearn.cluster import KMeans\n'+
                        f'kmeans = KMeans(n_clusters={self.n_clust})\n'+
                        f'kmeans_fit=kmeans.fit({self.name}.values)\nlabels=kmeans.fit_predict({self.name}.values)')

        else:
            with open(f'jupyter_notebook_{sid}.ipynb', 'a') as f:
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
                        f'\tclusters = estimator.fit_predict({self.name}.values)\n' +
                        f'\tscore = metrics.silhouette_score({self.name}.values, clusters)\n' +
                        '\treturn score\n\n'+
                        ']},')
                f.write('{ "cell_type": "code",' +
                        '"execution_count": 0,' +
                        '"metadata": {},' +
                        '"outputs": [],' +
                        '"source": [' +
                        'param_grid = {"n_clusters": range')
                f.write(f'({self.min}, {self.max})'+'}\n')
                f.write('search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)\n'+
                        f'grid = search.fit({self.name}.values)\n'+
                        'kmeans = grid.best_estimator_\n'+
                        f'kmeans_fit = kmeans.fit({self.ds}.values)\n'+
                        f'labels = kmeans.fit_predict({self.ds}.values)\n'+
                        ']},')
            f.close()

            with open(f'python_script_{sid}.py', 'a') as f:
                f.write('from sklearn.cluster import KMeans\n' +
                        'from sklearn.model_selection import GridSearchCV\n'+
                        'from sklearn import *\n'+
                        'def silhouette_score(estimator, X):\n'+
                        f'\tclusters = estimator.fit_predict({self.name}.values)\n'+
                        f'\tscore = metrics.silhouette_score({self.name}.values, clusters)\n'+
                        '\treturn score\n\n'+
                        'param_grid = {"n_clusters":'+ f'range({self.min}, {self.max})'+'}\n'+
                        'search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)\n'+
                        f'grid = search.fit({self.name}.values)\n' +
                        'kmeans = grid.best_estimator_\n'+
                        f'kmeans_fit = kmeans.fit({self.name}.values)\n'+
                        f'labels = kmeans.fit_predict({self.name}.values)\n')
            f.close()




'''
optimizations:
- select only some regions
- order by optimization
'''