from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn import *
def silhouette_score(estimator, X):
	clusters = estimator.fit_predict(table.values)
	score = metrics.silhouette_score(table.values, clusters)
	return score

param_grid = {"n_clusters":range(2, 8)}
search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)
grid = search.fit(table.values)
labels=search.fit_predict(table.values)
from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn import *
def silhouette_score(estimator, X):
	clusters = estimator.fit_predict(table.values)
	score = metrics.silhouette_score(table.values, clusters)
	return score

param_grid = {"n_clusters":range(2, 10)}
search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)
grid = search.fit(table.values)
labels=search.fit_predict(table.values)
from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn import *
def silhouette_score(estimator, X):
	clusters = estimator.fit_predict(table.values)
	score = metrics.silhouette_score(table.values, clusters)
	return score

param_grid = {"n_clusters":range(2, 4)}
search = GridSearchCV(KMeans(),param_grid=param_grid,scoring=silhouette_score)
grid = search.fit(table.values)
labels=search.fit_predict(table.values)
from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans_fit=kmeans.fit(table.values)
labels=kmeans.fit_predict(table.values)from sklearn.decomposition import PCA
pca = PCA(2)
pca_data = pca.fit_transform(table.values)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
u_labels = np.unique(labels)
for i in u_labels:
	plt.scatter(pca_data[labels == i, 0], pca_data[labels == i, 1], label=i)]
plt.legend()
plt.show()
