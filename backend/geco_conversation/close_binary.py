
from data_structure.dataset import Dataset
from .metadata_action import MetadataAction
from geco_conversation import *


class CloseBinary(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent == "affirm":
            return [Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)], None, {}
        else:
            return [Utils.chat_message("Do you want to go back to the selection?")], None, {}
