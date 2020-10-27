from .abstract_action import AbstractAction
from .start_action import StartAction
from geco_conversation import *

class ProjectMetaAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from .gmql_unary_action import GMQLUnaryAction
        from .gmql_binary_action import GMQLBinaryAction
        if 'change_meta' not in self.status:
            self.status['change_meta'] = message
            self.context.add_bot_msgs([Utils.chat_message('Which operation do you want to do?'), Utils.choice('Operators',{'sum':'+','difference':'-','product':'*','division':'/'})])
            return None, False
        elif 'operation' not in self.status:
            self.status['operation'] = message
            if message=='+':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the value you want to add'))
            elif message=='-':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the value you want to subtract'))
            elif message=='*':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the factor'))
            else:
                self.context.add_bot_msg(Utils.chat_message('Please, insert the divider'))
            return None, False
        elif 'value' not in self.status:
            self.status['value'] = int(message)
            self.context.add_bot_msg(Utils.chat_message('Do you want to rename the metadatum?\nIf so, provide a name'))
            return None, False
        elif 'new_name' not in self.status:
            if intent!='deny':
                self.status['new_name']=message
            else:
                self.status['new_name']=self.status['change_meta']
            change_dict = {self.status['new_name']: self.status['change_meta']+self.status['operation']+str(self.status['value'])}
            self.context.workflow.add(ProjectMetadata(self.context.workflow[-1],change_dict=change_dict))

            self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

class ProjectRegionAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from .gmql_unary_action import GMQLUnaryAction
        from .gmql_binary_action import GMQLBinaryAction
        if 'change_region' not in self.status:
            self.status['change_region'] = message
            self.context.add_bot_msgs([Utils.chat_message('Which operation do you want to do?'),
                                       Utils.choice('Operators',{'sum': '+', 'difference': '-', 'product': '*', 'division': '/'})])
            return None, False
        elif 'operation' not in self.status:
            self.status['operation'] = message
            if message == '+':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the value/region you want to add'))
            elif message == '-':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the value/region you want to subtract'))
            elif message == '*':
                self.context.add_bot_msg(Utils.chat_message('Please, insert the factor'))
            else:
                self.context.add_bot_msg(Utils.chat_message('Please, insert the divider'))
            return None, False
        elif 'value' not in self.status:
            if message.isnumeric():
                self.status['value'] = int(message)
            else:
                self.status['value'] = message
            self.context.add_bot_msg(Utils.chat_message('Do you want to rename the region datum?\nIf so, provide a name'))
            return None, False
        elif 'new_name' not in self.status:
            if intent != 'deny':
                self.status['new_name'] = message
            else:
                self.status['new_name'] = self.status['change_region']
            change_dict = {self.status['new_name']: self.status['change_region'] + self.status['operation'] + str(
                self.status['value'])}
            self.context.workflow.add(ProjectRegion(self.context.workflow[-1], change_dict=change_dict))
            self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

