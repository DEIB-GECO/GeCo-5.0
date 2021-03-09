from sklearn.decomposition import PCA
from .kmeans_logic import ClusteringRes

class PCARes:
    def __init__(self, data):
        self.pca_data = data


class PCALogic:
    def __init__(self, pca, sid):
        self.op = pca
        self.ds = self.op.depends_on.result
        if isinstance(self.ds, ClusteringRes):
            self.name = self.ds.name
            self.ds = self.ds.values
        self.components = pca.components
        self.run(sid)

    def run(self,sid):
        text = 'from sklearn.decomposition import PCA\n'
        pca = PCA(self.components)
        text += f'pca = PCA({self.components})\n'
        pca_data = pca.fit_transform(self.ds)
        text += f'pca_data = pca.fit_transform({self.name}.values)\n'
        self.op.result = PCARes(pca_data)
        self.op.executed = True
        self.write_script(sid, text)

    def write_script(self, sid, text):
        with open(f'python_script_{sid}.py', 'a') as f:
            f.write(text)

    def write(self,sid):
        with open(f'jupyter_notebook_{sid}.ipynb', 'a') as f:
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    '"source": [from sklearn.decomposition import PCA\n]},')
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    f'"source": [pca = PCA({self.components})\n' +
                    f'pca_data = pca.fit_transform({self.name}.values)\n]'+'},')
        f.close()

        with open(f'python_script_{sid}.py', 'a') as f:
            f.write('from sklearn.decomposition import PCA\n' +
                    f'pca = PCA({self.components})\n' +
                    f'pca_data = pca.fit_transform({self.name}.values)\n')
        f.close()