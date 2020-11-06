from geco_conversation import *

class NewDataset(AbstractAction):
    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
        return None, False

    def logic(self, message, intent, entities):
        if intent=='affirm':
            return StartAction(self.context), True
        elif intent=='deny':
            if len(self.context.data_extraction.datasets)%2==0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return PivotAction(self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.not_understood)])
            return None, False