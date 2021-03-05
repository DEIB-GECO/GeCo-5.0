import numpy as np
import matplotlib.pyplot as plt
from .kmeans_logic import ClusteringRes
from .pca_logic import PCARes

class ScatterRes:
    def __init__(self,x,y,labels,u_labels):
        self.x = x
        self.y = y
        self.labels = labels
        self.u_labels = u_labels

class ScatterLogic:
    def __init__(self, scatter):
        self.op = scatter
        self.ds = self.op.depends_on.result
        #self.df = scatter.df
        if isinstance(self.ds, PCARes):
            self.ds = self.ds.pca_data
        self.labels = self.op.depends_on_2.result
        if isinstance(self.labels, ClusteringRes):
            self.labels = self.labels.labels
        self.run()

    def run(self):
        print(self.ds)
        print(self.ds.shape)
        u_labels = np.unique(self.labels)
        print('labels', self.labels)
        for i in u_labels:
            plt.scatter(self.ds[self.labels == i, 0], self.ds[self.labels == i, 1], label=i)
         #   print('0',self.ds[self.labels == i, 0])
        #    print('1', self.ds[self.labels == i, 1])
        #plt.legend()
        #plt.show()
        self.op.result = ScatterRes(self.ds[:, 0], self.ds[:, 1], self.labels, u_labels)
        self.op.executed = True
        self.write()

    def write(self):
        with open('jupyter_notebook.ipynb', 'a') as f:
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    '"source": [import matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np]},')
            f.write('{ "cell_type": "code",' +
                    '"execution_count": 0,' +
                    '"metadata": {},' +
                    '"outputs": [],' +
                    '"source": [u_labels = np.unique(labels)\n'
                    'for i in u_labels:\n\t'
                    'plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]\n'
                    'plt.legend()\n'
                    'plt.show()},')
        f.close()

        with open('python_script.py', 'a') as f:
            f.write('import matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np\n' +
                    'u_labels = np.unique(labels)\n'
                    'for i in u_labels:\n\t'
                    'plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]\n'
                    'plt.legend()\n'
                    'plt.show()\n')
        f.close()