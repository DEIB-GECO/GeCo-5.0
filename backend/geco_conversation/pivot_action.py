from geco_conversation import *

class PivotAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def logic(self, message, intent, entities):
        return [Utils.chat_message("OK, which metadata do you want to keep in the columns?")], None, {}
