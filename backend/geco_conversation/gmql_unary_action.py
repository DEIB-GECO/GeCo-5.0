from .abstract_action import AbstractAction
from geco_conversation import *

class GMQLUnaryAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.gmql_unary))
        self.context.add_bot_msg(Utils.choice('Unary_operations',{'Project metadata':'project metadata', 'Project region':'project region', 'Cover':'cover'}))
        return None, False

    def logic(self, message, intent, entities):
        bool = False
        if intent == 'project_metadata':
            #self.context.add_bot_msg(Utils.chat_message(messages.modify_metadata))
            self.context.add_bot_msg(Utils.workflow('Project Metadata'))
            next_node = ProjectKeepMetaAction(self.context)
            bool = True
        elif intent == 'project_region':
            #self.context.add_bot_msg(Utils.chat_message(messages.modify_region))
            self.context.add_bot_msg(Utils.workflow('Project Region'))
            next_node = ProjectKeepRegionAction(self.context)
            bool = True
        elif intent == 'keep_metadata':
            self.payload.insert('back', ProjectMetaAction)
            self.context.add_bot_msgs([Utils.chat_message(messages.keep_meta), Utils.workflow('Project Metadata')])
            next_node = KeepAction(self.context)
        elif intent == 'keep_region':
            self.payload.insert('back', ProjectRegionAction)
            self.context.add_bot_msg(Utils.chat_message(messages.keep_region))
            self.context.add_bot_msg(Utils.workflow('Project Region'))
            next_node = KeepAction(self.context)
        elif intent == 'cover':
            self.context.add_bot_msg(Utils.chat_message(messages.cover_message))
            self.context.add_bot_msg(Utils.workflow('Cover'))
            next_node = CoverAction(self.context)
            bool = False
        else:
            self.context.add_bot_msg(Utils.chat_message(messages.not_understood))
            next_node = None
            bool = False
        return next_node, bool
