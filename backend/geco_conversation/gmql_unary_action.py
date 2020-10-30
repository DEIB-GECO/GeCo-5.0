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
            self.context.add_bot_msg(Utils.chat_message(messages.modify_metadata))
            next_node = ProjectMetaAction(self.context)
            bool = False
        elif intent == 'project_region':
            self.context.add_bot_msg(Utils.chat_message(messages.modify_region))
            next_node = ProjectRegionAction(self.context)
        elif intent == 'cover':
            self.context.add_bot_msg(Utils.chat_message(messages.cover_message))
            next_node = CoverAction(self.context)
            bool = False
        else:
            self.context.add_bot_msg(Utils.chat_message(messages.not_understood))
            next_node = None
            bool = False
        return next_node, bool
