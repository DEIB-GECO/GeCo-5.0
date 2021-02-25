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
