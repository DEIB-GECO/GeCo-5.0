from .abstract_action import AbstractAction
from .union_action import UnionAction
from .join_action import JoinAction
from geco_conversation import *

class GMQLBinaryAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.binary_help)]

    def on_enter(self):
        self.context.add_bot_msgs(
            [Utils.chat_message(messages.gmql_binary),
             Utils.choice('Binary_operations',{'Join':'join', 'Union':'union', 'Difference':'difference', 'Map':'map'})])
        return None, False


    def logic(self, message, intent, entities):
        bool = True
        if intent == 'join':
            self.context.add_bot_msgs([Utils.chat_message("Do you want to add a metadatum for the joinby?\n If so, which one?")])
            next_node = JoinAction(self.context)
            bool = False
        elif intent == 'union':
            self.context.add_bot_msgs([Utils.chat_message("Ok. I will do the union of the two datasets")])
            next_node = UnionAction(self.context)
        elif intent == 'difference':
            self.context.add_bot_msgs([Utils.chat_message("Ok. I will do the difference of the two datasets")])
            next_node = DifferenceAction(self.context)
        elif intent == 'map':
            self.context.add_bot_msgs([Utils.chat_message("Which aggregate function do you want?")])
            next_node = MapAction(self.context)
            bool = False
        else:
            self.context.add_bot_msg([Utils.chat_message("Sorry, I did not get. Which operation do you want to perform?")])
            next_node = None
            bool = False
        return next_node, bool
