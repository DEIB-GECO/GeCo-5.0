from geco_conversation import *


class KMeansClustering(AbstractAction):

    def help_message(self):
        pass

    def on_enter(self):
        self.context.add_bot_msg(
            Utils.chat_message("Do you already know how many clusters to create? If so, tell me the number"))

        self.context.add_bot_msg(
            Utils.workflow("KMeans Clustering"))
        return None, False

    def logic(self, message, intent, entities):

        if intent != 'deny':
            n_clust = int(''.join(filter(str.isdigit, message)))
            # self.context.add_bot_msg(
            #   Utils.chat_message("Ok, I will perform K-Means clustering using {}.".format(n_clust)))
            self.context.workflow.add(KMeans(self.context.workflow[-1], clusters=n_clust))
            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
            self.context.workflow.run(self.context.workflow[-1],self.context.session_id)
            # print(self.context.workflow[-1].result.__dict__)
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            self.context.add_bot_msg(Utils.chat_message(f"Ok, I did K-Means clustering using {n_clust}."))
            return ByeAction(self.context), True

        else:
            self.context.add_bot_msg(Utils.chat_message(messages.min_n_clust))
            return NumClusters(self.context), False


class NumClusters(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if not hasattr(self, 'min'):
            self.min = int(''.join(filter(str.isdigit, message)))
            self.context.add_bot_msg(Utils.chat_message(messages.max_n_clust))
            return None, False
        else:
            self.max = int(''.join(filter(str.isdigit, message)))
            self.context.add_bot_msg(Utils.chat_message(messages.analysis_done))
            self.context.workflow.add(KMeans(self.context.workflow[-1], tuning=True, min=self.min, max=self.max))
            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
            self.context.workflow.run(self.context.workflow[-1],self.context.session_id)
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            self.context.add_bot_msg(
                Utils.param_list(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            #self.context.add_bot_msg(Utils.chat_message(messages.restart))
            self.context.add_bot_msg(Utils.chat_message("Do you want to do again the K-Means Clustering?"))
            return YesNoAction(self.context, KMeansClustering(self.context), ByeAction(self.context)), False