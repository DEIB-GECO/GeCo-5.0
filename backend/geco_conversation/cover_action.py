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
                self.context.add_bot_msg(Utils.chat_message('Sorry I didn\'t understand, choose a number for the minimum or write any'))

            self.context.add_bot_msg(Utils.chat_message('Now please choose the maximum.'))
            return None, False

        elif 'max' not in self.status:
            if message.lower()=='any':
                self.status['max']='ANY'
            elif message.isnumeric():
                self.status['max'] = int(message)
            else:
                self.context.add_bot_msg(Utils.chat_message('Sorry I didn\'t understand, choose a number for the maximum or write any'))

            self.context.add_bot_msg(Utils.chat_message('Do you want to groupby? If so, provide a metadatum on which groupby.'))

            return None, False
        elif 'groupby' not in self.status:
            if intent!='deny':
                self.status['groupby'] = message
                self.context.workflow.add(Cover(self.context.workflow[-1],self.status['min'], self.status['max'],self.status['groupby']))
            else:
                self.context.workflow.add(Cover(self.context.workflow[-1],self.status['min'], self.status['max']))
            self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False


