from geco_conversation import AbstractAction
from geco_utilities import Utils, helpMessages, messages


class RenameAction(AbstractAction):
    def __init__(self, context, next_action):
        super().__init__(context)
        self.next = next_action

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.rename_help)])
        return None, True

    def on_enter(self):
        self.context.add_bot_msg(Utils.choice('',{}))
        self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
        return None, False

    def logic(self, message, intent, entities):
        if intent == "affirm":
            self.context.add_bot_msgs([Utils.chat_message(messages.name)])
            return None, False
        elif intent=='deny':
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )
        else:
            name = message.strip()
        self.context.payload.update('fields', {'name':name})
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x not in ['metadata','regions']}
        self.context.add_bot_msgs([Utils.chat_message("OK, dataset saved with name: " + name),#Utils.chat_message(messages.download),
                Utils.param_list(list_param)])
        return self.next, True