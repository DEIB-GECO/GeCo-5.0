from sklearn.cluster import KMeans

class KMeansLogic:
    def __init__(self, kmeans):
        self.op = kmeans
        self.ds = self.op.depends_on.result
        self.tuning = kmeans.tuning
        if self.tuning:
            self.min = kmeans.min
            self.max = kmeans.maxKMeans
            self.run_tuned()
        else:
            self.n_clust = kmeans.n_clust
            self.run()

    def run(self):
        kmeans = KMeans(n_clusters=self.n_clust).fit(self.ds.values)



