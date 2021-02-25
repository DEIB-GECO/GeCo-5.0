from geco_conversation import *

class DataAnalysis(AbstractAction):

    def help_message(self):
        self.context.add_bot_msg("")
        return None, False

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message("Which operation do you want to do?"))
        self.context.add_bot_msg(Utils.choice('Available operations', {'K-Means clustering': 'K-Means clustering'}))
        return None, False

    def logic(self, message, intent, entities):

        if intent in ['clustering','cluster']:
            self.context.add_bot_msg(Utils.chat_message("Ok, I will perform K-Means clustering."))
            return Clustering(self.context), True

        else:
            self.context.add_bot_msg(Utils.chat_message("Sorry, only clustering is implemented till now."))
            return None, True
