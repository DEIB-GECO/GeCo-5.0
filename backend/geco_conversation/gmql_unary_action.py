from .abstract_action import AbstractAction
from geco_conversation import *

class GMQLUnaryAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.gmql_unary))
        self.context.add_bot_msg(Utils.choice('Unary_operations',{'project_metadata':'project metadata', 'project_region':'project region', 'cover':'cover'}))
        return None, False

    def logic(self, message, intent, entities):
        bool = False
        if intent == 'project_metadata':
            self.context.add_bot_msg(Utils.chat_message("Which metadata do you want to modify?"))
            next_node = ProjectMetaAction(self.context)
        elif intent == 'project_region':
            self.context.add_bot_msg(Utils.chat_message("Which region data do you want to modify?"))
            next_node = ProjectRegionAction(self.context)
        elif intent == 'cover':
            self.context.add_bot_msg(Utils.chat_message("I need you to tell me the min, max and, optionally, the groupby.\nLet's begin with the min."))
            next_node = CoverAction(self.context)
            bool = False
        else:
            self.context.add_bot_msg(Utils.chat_message("Sorry, I did not understand. Can you repeat?"))
            next_node = None
            bool = False
        return next_node, bool
