from .abstract_action import AbstractAction
from .start_action import StartAction
from geco_conversation import *
from data_structure.operations import ArithmeticOperation

class ProjectMetaAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from .gmql_unary_action import GMQLUnaryAction
        from .gmql_binary_action import GMQLBinaryAction
        self.payload.insert('back', ProjectMetaAction)
        if 'change_meta' not in self.status:
            self.context.payload.insert('change_meta', Field(message))
            self.context.add_bot_msgs([Utils.chat_message(messages.arithmetic_operation), Utils.choice('Operators',{'sum':'+','difference':'-','product':'*','division':'/'})])
            return None, False
        elif 'operation' not in self.status:
            if message=='+':
                self.context.payload.insert('operation', ArithmeticOperation.SUM.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.sum_meta))
            elif message=='-':
                self.context.payload.insert('operation', ArithmeticOperation.SUBTRACT.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.sub_meta))
            elif message=='*':
                self.context.payload.insert('operation', ArithmeticOperation.PRODUCT.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.factor))
            else:
                self.context.payload.insert('operation', ArithmeticOperation.DIVISION.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.divider))
            return None, False
        elif self.status['operation'][0].op2==None:
            if message.isnumeric():
                self.context.payload.update('operation', self.status['operation'][0].parameters(self.status['change_meta'][0], float(message)))
            else:
                self.context.payload.update('operation',
                                    self.status['operation'][0].parameters(self.status['change_meta'][0], Field(message)))
            self.context.add_bot_msg(Utils.chat_message(messages.rename_meta))
            return None, False
        elif 'new_name' not in self.status:
            if intent!='deny':
                self.status['new_name']=message
            else:
                self.status['new_name']=self.status['change_meta']
            change_dict = {self.status['new_name']: self.status['operation'][0]}

            self.context.workflow.add(ProjectMetadata(self.context.workflow[-1],change_dict=change_dict))
            self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
            self.context.payload.clear()
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
            self.context.payload.insert('change_region', Field(message))
            self.context.add_bot_msgs([Utils.chat_message(messages.arithmetic_operation),
                                       Utils.choice('Operators',{'sum': '+', 'difference': '-', 'product': '*', 'division': '/'})])
            return None, False
        elif 'operation' not in self.status:
            if message == '+':
                self.context.payload.insert('operation', ArithmeticOperation.SUM.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.sum_region))
            elif message == '-':
                self.context.payload.insert('operation', ArithmeticOperation.SUBTRACT.parameters())
                self.context.add_bot_msg(
                    Utils.chat_message(messages.sub_region))
            elif message == '*':
                self.context.payload.insert('operation', ArithmeticOperation.PRODUCT.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.prod_region))
            else:
                self.context.payload.insert('operation', ArithmeticOperation.DIVISION.parameters())
                self.context.add_bot_msg(Utils.chat_message(messages.div_region))
            return None, False
        elif self.status['operation'][0].op2 == None:
            if message.isnumeric():
                self.context.payload.update('operation',
                                    self.status['operation'][0].parameters(self.status['change_region'][0], float(message)))
            else:
                self.context.payload.update('operation',
                                    self.status['operation'][0].parameters(self.status['change_region'][0], Field(message)))
            # self.status['operation'] = int(message)
            self.context.add_bot_msg(Utils.chat_message(messages.rename_region))
            return None, False
        elif 'new_name' not in self.status:
            if intent != 'deny':
                self.context.payload.insert('new_name', message)
            else:
                self.context.payload.insert('new_name', self.status['change_region'])
            change_dict = {self.status['new_name']: self.status['operation'][0]}
            self.context.workflow.add(ProjectRegion(self.context.workflow[-1], change_dict=change_dict))
            self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
            self.context.payload.clear()
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False


class KeepAction(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if self.status['back']=='ProjectMetaAction':
            values = message.lower().strip().split(';')
            values = [Field(x) for x in values]
            self.context.workflow.add(ProjectMetadata(self.context.workflow[-1], keep_list=values))
            self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
        else:
            values = message.lower().strip().split(';')
            values = [Field(x) for x in values]
            self.context.workflow.add(ProjectRegion(self.context.workflow[-1], keep_list=values))
            self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
            if len(self.context.data_extraction.datasets) % 2 == 0:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
            else:
                return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

