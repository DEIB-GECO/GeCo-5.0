from geco_conversation import *


class Clustering(AbstractAction):

    def on_enter(self):
        self.context.add_bot_msg("Do you already know how many clusters to create? If so, tell me the number")

    def logic(self, message, intent, entities):

        if intent != 'deny':
            n_clust = int(filter(str.isdigit, message))
            self.context.add_bot_msg("Ok, I will perform K-Means clustering using {}.".format(n_clust))
            self.context.workflow.add(KMeans(self.context.workflow[-1], clusters=n_clust))
            return Clustering(self.context), True

        else:
            self.context.add_bot_msg("Which is the minimum number of clusters you want to try?")
            return NumClusters(self.context), False

class NumClusters(AbstractAction):
    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if not hasattr(self,'min'):
            self.min = int(filter(str.isdigit, message))
            self.context.add_bot_msg("Which is the maximum number of clusters you want to try?")
        else:
            self.max = int(filter(str.isdigit, message))
            self.context.add_bot_msg("Ok, I will perform K-Means clustering using parameter tuning trying many cluster numbers between {} and {}.".format(self.min,self.max))
            self.context.workflow.add(KMeans(self.context.workflow[-1], tuning=True, min=self.min, max=self.max))