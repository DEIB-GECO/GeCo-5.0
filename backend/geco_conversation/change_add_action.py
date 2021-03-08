from data_structure.database import experiment_fields
from geco_conversation import *


class ChangeAddAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.change_add_help)])
        return None, False

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent == 'change_option':
            self.context.payload.delete(self.status['field'])
            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields}

            if len(gcm_filter) > 0:
                self.db.update(gcm_filter)
            return ValueAction(self.context), False

        elif intent == 'add_option':
            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields and k != self.status['field']}

            if len(gcm_filter) > 0:
                self.db.update(gcm_filter)
            list_param = {x: x for x in self.context.payload.original_db.values[self.status['field']]}
            choice = [True if len(list_param) > 10 else False]
            self.context.add_bot_msgs([Utils.chat_message(f"Please provide a {self.status['field']}"),
                                       Utils.choice(self.status['field'], list_param, show_search=choice)])
            return ValueAction(self.context), False
        else:
            gcm_filter = {k: v for (k, v) in self.status.items() if
                          k in self.db.fields and k != self.status['field']}

            if len(gcm_filter) > 0:
                self.db.update(gcm_filter)
            list_param = {x: x for x in self.db.fields}
            self.context.add_bot_msgs([Utils.chat_message(
                f"Sorry, I didn't understand. Do you want to change or add a new {self.status['field']}?"),
                                       Utils.choice('Available fields', list_param)])
            return None, False
