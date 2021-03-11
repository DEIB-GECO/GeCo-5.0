from geco_conversation import *


class KMeansClustering(AbstractAction):

    def help_message(self):
        pass

    def on_enter(self):
        print('status', self.status)
        if self.context.workflow[-1].__class__.__name__ == 'Pivot':
            self.context.payload.insert('Ds Name', self.context.workflow[-1].result.name)
        else:
            for i in range((len(self.context.workflow) - 2), 0, -1):
                if self.context.workflow[i].__class__.__name__ == 'Pivot':
                    self.context.payload.insert('Ds Name', self.context.workflow[i].result.name)
        self.context.payload.insert('Method', 'KMeans Clustering')
        self.context.add_bot_msg(Utils.param_list({k: v[0] for k, v in self.status.items()}))
        self.context.add_bot_msg(
            Utils.chat_message(
                "Do you already know how many clusters to create? If so, tell me the number, otherwise I will apply parameter tuning."))

        self.context.add_bot_msg(
            Utils.workflow("KMeans Clustering"))
        return KMeansClustering(self.context), False

    def logic(self, message, intent, entities):

        if intent != 'deny':
            n_clust = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('N° clusters', n_clust)
            Utils.wait_msg('Please wait, this step can take some time.')
            import time
            time.sleep(0.5)
            if self.context.workflow[-1].__class__.__name__ == 'Pivot':
                self.context.workflow.add(KMeans(self.context.workflow[-1], clusters=n_clust))
            else:
                for i in range((len(self.context.workflow) - 2), 0, -1):
                    if self.context.workflow[i].__class__.__name__ == 'Pivot':
                        self.context.workflow.add(KMeans(self.context.workflow[i], clusters=n_clust))
            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
            self.context.workflow.run(self.context.workflow[-1], self.context.session_id)
            # print(self.context.workflow[-1].result.__dict__)
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            self.context.add_bot_msg(Utils.chat_message(f"Ok, I did K-Means clustering using {n_clust}."))
            self.context.add_bot_msg(Utils.param_list({k: v[0] for k, v in self.status.items()}))
            self.context.add_bot_msg(Utils.chat_message("Do you want to do again the K-Means Clustering?"))
            return YesNoAction(self.context, KMeansClustering(self.context), ByeAction(self.context)), False

        else:
            self.context.add_bot_msg(Utils.chat_message(messages.par_tuning_kmeans))
            self.context.add_bot_msg(Utils.chat_message(messages.min_n_clust))
            return NumClusters(self.context), False


class NumClusters(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        print(self.status)
        if 'Min N° Clusters' not in self.status:
            min = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('Min N° Clusters', min)
            self.context.add_bot_msg(Utils.param_list({k: v[0] for k, v in self.status.items()}))
            print('status after min', self.status)
            self.context.add_bot_msg(Utils.chat_message(messages.max_n_clust))
            return NumClusters(self.context), False
        else:
            max = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('Max N° Clusters', max)
            Utils.wait_msg('Please wait, this step can take some time.')
            import time
            time.sleep(0.5)
            self.context.add_bot_msg(Utils.chat_message(messages.analysis_done))
            if self.context.workflow[-1].__class__.__name__ == 'Pivot':
                self.context.workflow.add(
                    KMeans(self.context.workflow[-1], tuning=True, min=self.status['Min N° Clusters'][0],
                           max=self.status['Max N° Clusters'][0]))
            else:
                for i in range((len(self.context.workflow) - 2), 0, -1):
                    if self.context.workflow[i].__class__.__name__ == 'Pivot':
                        self.context.workflow.add(
                            KMeans(self.context.workflow[i], tuning=True, min=self.status['Min N° Clusters'][0],
                                   max=self.status['Max N° Clusters'][0]))

            self.context.workflow.add(PCA(self.context.workflow[-1], 2))
            self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))

            self.context.workflow.run(self.context.workflow[-1], self.context.session_id)
            self.context.payload.insert('N° Clusters', len(self.context.workflow[-1].result.u_labels))
            self.context.add_bot_msg(Utils.param_list({k: v[0] for k, v in self.status.items()}))
            self.context.add_bot_msg(
                Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                              self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
            # self.context.add_bot_msg(Utils.chat_message(messages.restart))
            self.context.add_bot_msg(Utils.chat_message("Do you want to do again the K-Means Clustering?"))
            self.context.payload.clear()
            return YesNoAction(self.context, KMeansClustering(self.context), ByeAction(self.context)), False
