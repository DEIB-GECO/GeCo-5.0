from .abstract_action import AbstractAction
from .start_action import StartAction
from geco_conversation import *

class ProjectMetaAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if 'change_meta' not in self.status:
            self.status['change_meta'] = message
            self.context.add_bot_msgs([Utils.chat_message('Which operation do you want to do?'), Utils.choice({'sum':'+','difference':'-','product':'*','division':'/'})])
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
            self.context.workflow.add_gmql('project_metadata',{'Dataset':self.context.data_extraction.datasets[-1],'New':{self.status['new_name']:"{}{}{}".format(self.status['change_meta'],self.status['operation'],self.status['value'])}})
            return None, False

        self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
        return GMQLUnaryAction(self.context), False

class ProjectRegionAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if 'change_region' not in self.status:
            self.status['change_region'] = message
            self.context.add_bot_msgs([Utils.chat_message('Which operation do you want to do?'),
                                       Utils.choice({'sum': '+', 'difference': '-', 'product': '*', 'division': '/'})])
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
            self.context.workflow.add_gmql('project_regions', {'Dataset': self.context.data_extraction.datasets[-1],
                                                                'New': {self.status['new_name']: "{}{}{}".format(
                                                                    self.status['change_region'],
                                                                    self.status['operation'], self.status['value'])}})
            self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
            return GMQLUnaryAction(self.context), False

