from .abstract_action import AbstractAction
from .union_action import UnionAction
from .join_action import JoinAction
from geco_conversation import *

class BinaryAction(AbstractAction):


    def help_message(self):
        return [Utils.chat_message(helpMessages.unary_help)]


    def logic(self, message, intent, entities):
        if intent == 'project_metadata':
            msg = [Utils.chat_message('Sorry, this option is not implemented yet.')]
            next_node = JoinAction({})
        elif intent == 'project_region':
            msg = [Utils.chat_message('Sorry, this option is not implemented yet.')]
            next_node = UnionAction({})
        elif intent == 'cover':
            msg = [Utils.chat_message('Sorry, this option is not implemented yet.')]
            next_node = None
        else:
            msg = [Utils.chat_message("Sorry, I did not get. Which operation do you want to perform?")]
            next_node = None
        self.context.add_bot_msgs(msg)
        return next_node, False
