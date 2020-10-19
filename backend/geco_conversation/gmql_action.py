from .abstract_action import AbstractAction
from .start_action import StartAction

class GmqlAction(AbstractAction):

    def help_message(self):
        return []

    def logic(self, message, intent, entities):
        if message is None:
            self.context.add_bot_msgs(Utils.chat_message(messages.gmql_operations))
            return None, False
        else:
            self.context.add_bot_msg(
                [Utils.chat_message("Sorry, this is not implemented yet")])
            next_node = None
        return next_node, True
