from geco_conversation import AbstractAction
from geco_utilities import Utils, helpMessages, messages


class RenameAction(AbstractAction):
    def __init__(self, context, next_action):
        super().__init__(context)
        self.next = next_action

    def help_message(self):
        return [Utils.chat_message(helpMessages.rename_help)]

    def on_enter(self):
        self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
        return None, False

    def logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )

        urls = self.context.payload.database.download(self.status['fields'])
        self.context.payload.update('fields', {'name':name})
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        self.context.add_bot_msgs([Utils.chat_message("OK, dataset saved with name: " + name),Utils.chat_message(messages.download),
                Utils.param_list(list_param), Utils.workflow('Data selection', True, urls)])
        return self.next, True