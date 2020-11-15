from .abstract_action import AbstractAction
from .start_action import StartAction
from geco_conversation import *
from data_structure.operations import ArithmeticOperation

class ProjectKeepMetaAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(
            "Do you want to modify one or many metadata or do you want to tell me the ones you want to keep?"))
        return None, False

    def logic(self, message, intent, entities):
        self.context.payload.insert('back', ProjectMetaAction)
        if intent=='project_metadata':
            return ProjectMetaAction(self.context), True
        else:
            return KeepAction(self.context), True

class ProjectKeepRegionAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(
            "Do you want to modify one or many regions or do you want to tell me the ones you want to keep?"))
        return None, False

    def logic(self, message, intent, entities):
        self.context.payload.insert('back', ProjectRegionAction)
        if intent == 'project_region':
            return ProjectMetaAction(self.context), True
        else:
            return KeepAction(self.context), True


class KeepAction(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.keep))
        return None, False

    def logic(self, message, intent, entities):
        if isinstance(self.status['back'],ProjectMetaAction):
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

