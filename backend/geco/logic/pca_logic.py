from sklearn.decomposition import PCA
from .kmeans_logic import ClusteringRes

class PCARes:
    def __init__(self, data):
        self.pca_data = data


class PCALogic:
    def __init__(self, pca):
        self.op = pca
        self.ds = self.op.depends_on.result
        if isinstance(self.ds, ClusteringRes):
            self.ds = self.ds.values
        self.components = pca.components
        self.run()

    def run(self):
        pca = PCA(self.components)
        pca_data = pca.fit_transform(self.ds)
        self.op.result = PCARes(pca_data)
        self.op.executed = True
        self.write()

    def write(self):
        with open('jupyter_notebook.ipynb', 'a') as f:
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    '"source": [from sklearn.decomposition import PCA\n]},')
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    '"source": [pca = PCA({})\n' + 'pca_data = pca.fit_transform(table.values)\n]},')
        f.close()

        with open('python_script.py', 'a') as f:
            f.write('from sklearn.decomposition import PCA\n' +
                    'pca = PCA({})\n'.format(self.components) + 'pca_data = pca.fit_transform(table.values)\n'.format(self.components))
        f.close()