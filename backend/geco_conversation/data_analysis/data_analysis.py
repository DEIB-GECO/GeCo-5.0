from geco_conversation import *

class DataAnalysis(AbstractAction):

    def help_message(self):
        #self.context.add_bot_msg("")
        return None, False

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.arithmetic_operation))
        self.context.add_bot_msg(Utils.choice('Available operations', {'K-Means clustering': 'K-Means clustering', 'DBScan clustering': 'DBScan Clustering'}))
        return DataAnalysis(self.context), False

    def logic(self, message, intent, entities):

        if intent in ['clustering','cluster']:
            self.context.add_bot_msg(Utils.chat_message(messages.kmeans))
            return KMeansClustering(self.context), True
        elif intent=='kmeans':
            self.context.add_bot_msg(Utils.chat_message(messages.kmeans))
            return KMeansClustering(self.context), True
        elif intent=='dbscan':
            self.context.add_bot_msg(Utils.chat_message(messages.dbscan))
            return DBScanClustering(self.context), True
        else:
            self.context.add_bot_msg(Utils.chat_message(messages.only_clust))
            return DataAnalysis(self.context), True
