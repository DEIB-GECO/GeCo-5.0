from geco_conversation import *

class MapAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        pass