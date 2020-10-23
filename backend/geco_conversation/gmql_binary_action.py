from .abstract_action import AbstractAction
from .union_action import UnionAction
from .join_action import JoinAction
from geco_conversation import *

class GMQLBinaryAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.binary_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent == 'join':
            self.context.add_bot_msg([Utils.chat_message("Sorry, this option is not implemented yet.")])
            next_node = JoinAction(self.context)
        elif intent == 'union':
            self.context.add_bot_msg([Utils.chat_message("Sorry, this option is not implemented yet.")])
            next_node = UnionAction(self.context)
        elif intent == 'difference':
            self.context.add_bot_msg([Utils.chat_message("Sorry, this option is not implemented yet.")])
            next_node = DifferenceAction(self.context)
        else:
            self.context.add_bot_msg([Utils.chat_message("Sorry, I did not get. Which operation do you want to perform?")])
            next_node = JoinAction(self.context)
        return msg, next_node, new_status
