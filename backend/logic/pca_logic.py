from sklearn.decomposition import PCA
from .kmeans_logic import KMeansRes
class PCALogic:
    def __init__(self, pca):
        self.op = pca
        self.ds = self.op.depends_on.result
        if isinstance(self.ds, KMeansRes):
            self.ds = self.ds.values
        self.components = pca.components
        self.run()

    def run(self):
        pca = PCA(self.components)
        pca_data = pca.fit_transform(self.ds)
        self.op.result = pca_data
        self.op.executed = True
        self.write()

    def write(self):
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
                    '"source": [pca = PCA({})\n' + 'pca_data = pca.fit_transform(table.values)\n]},')
        f.close()

        with open('python_script.py', 'a') as f:
            f.write('from sklearn.cluster import KMeans\n' +
                    'pca = PCA({})\n'.format(self.components) + 'pca_data = pca.fit_transform(table.values)\n'.format(self.components))
        f.close()