from .abstract_action import AbstractAction
from .start_action import StartAction
from geco_conversation import *

class CoverAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from .gmql_unary_action import GMQLUnaryAction
        from .gmql_binary_action import GMQLBinaryAction
        if 'min' not in self.status:
            if message.lower()=='any':
                self.status['min']='ANY'
            elif message.isnumeric():
                self.status['min'] = int(message)
            else:
                self.context.add_bot_msg(Utils.chat_message(messages.cover_not_understood))

            self.context.add_bot_msg(Utils.chat_message(messages.choose_max))
            return None, False

        elif 'max' not in self.status:
            if message.lower()=='any':
                self.status['max']='ANY'
            elif message.isnumeric():
                self.status['max'] = int(message)
            else:
                self.context.add_bot_msg(Utils.chat_message(messages.cover_not_understood))

            self.context.add_bot_msg(Utils.chat_message(messages.groupby))

            return None, False
        elif 'groupby' not in self.status:
            if intent!='deny':
                self.status['groupby'] = Field(message)
                self.context.workflow.add(Cover(self.context.workflow[-1],self.status['min'], self.status['max'],self.status['groupby']))
            else:
                self.context.workflow.add(Cover(self.context.workflow[-1],self.status['min'], self.status['max']))
            self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
            self.context.payload.clear()
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

