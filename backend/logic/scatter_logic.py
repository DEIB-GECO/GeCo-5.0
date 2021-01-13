import numpy as np
import matplotlib.pyplot as plt
from .kmeans_logic import KMeansRes

class ScatterLogic:
    def __init__(self, scatter):
        self.op = scatter
        self.ds = self.op.depends_on.result
        #self.df = scatter.df

        self.labels = self.op.depends_on_2.result
        if isinstance(self.labels, KMeansRes):
            self.labels = self.labels.labels
        self.run()

    def run(self):
        #u_labels = np.unique(self.labels)

        #for i in u_labels:
        #    plt.scatter(self.df[self.labels == i, 0], self.df[self.labels == i, 1], label=i)

        #plt.legend()
        #plt.show()
        self.op.result = 'Figure'
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
                    'plt.scatter(df[labels == i, 0], df[labels == i, 1], label=i)]\n'
                    'plt.legend()\n'
                    'plt.show()},')
        f.close()

        with open('python_script.py', 'a') as f:
            f.write('import matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np' +
                    'u_labels = np.unique(labels)\n'
                    'for i in u_labels:\n\t'
                    'plt.scatter(df[labels == i, 0], df[labels == i, 1], label=i)]\n'
                    'plt.legend()\n'
                    'plt.show()')
        f.close()