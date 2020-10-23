from geco_conversation import *

class PivotAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.pivot_message)])
        self.context.add_bot_msgs([Utils.chat_message(messages.row_message)])

    def logic(self, message, intent, entities):
        pass
