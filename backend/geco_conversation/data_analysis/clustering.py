from geco_conversation import *


class Clustering(AbstractAction):

    def help_message(self):
        pass

    def on_enter(self):
        self.context.add_bot_msg(
            Utils.chat_message("Do you already know how many clusters to create? If so, tell me the number"))
        return None, False

    def logic(self, message, intent, entities):

        if intent != 'deny':
            n_clust = int(''.join(filter(str.isdigit, message)))
            #self.context.add_bot_msg(
             #   Utils.chat_message("Ok, I will perform K-Means clustering using {}.".format(n_clust)))
            self.context.workflow.add(KMeans(self.context.workflow[-1], clusters=n_clust))
            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
            self.context.workflow.run(self.context.workflow[-1])
            print(self.context.workflow[-1].result.__dict__)
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            self.context.add_bot_msg(Utils.chat_message("Ok, I did K-Means clustering using {}.".format(n_clust)))

            return ByeAction(self.context), True

        else:
            self.context.add_bot_msg(Utils.chat_message("Which is the minimum number of clusters you want to try?"))
            return NumClusters(self.context), False


class NumClusters(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if not hasattr(self, 'min'):
            self.min = int(''.join(filter(str.isdigit, message)))
            self.context.add_bot_msg(Utils.chat_message("Which is the maximum number of clusters you want to try?"))
            return None, False
        else:
            self.max = int(''.join(filter(str.isdigit, message)))
            self.context.add_bot_msg(Utils.chat_message(
                "Ok, I will perform K-Means clustering using parameter tuning trying many cluster numbers between {} and {}.".format(
                    self.min, self.max)))
            self.context.workflow.add(KMeans(self.context.workflow[-1], tuning=True, min=self.min, max=self.max))
            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
            self.context.workflow.run(self.context.workflow[-1])
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            return None, False
