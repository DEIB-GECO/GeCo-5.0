from data_structure.database import experiment_fields, annotation_fields
from geco_conversation import *


class FieldAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.fields_help)])
        return None, False

    def on_enter(self):
        pass

    def check_status(self):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k == 'is_healthy':
                if self.status['is_healthy'] == ['healthy']:
                    self.context.payload.insert('is_healthy', [True])
                if self.status['is_healthy'] == ['tumoral']:
                    self.context.payload.insert('is_healthy', [False])
            if k in self.db.fields and k != 'is_healthy':
                self.context.payload.replace(k, [x for x in v if x in self.db.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

    def filter(self, gcm_filter):
        if len(gcm_filter) > 0:
            self.db.update(gcm_filter)

        samples = self.db.check_existance(gcm_filter)

        return samples

    def logic(self, message, intent, entities):
        from .value_action import ValueAction, DSNameAction
        from .change_add_action import ChangeAddAction

        self.check_status()
        gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields}
        samples = self.filter(gcm_filter)
        if samples > 0:
            if intent != 'deny':
                field = entities['field'] if 'field' in entities else [message.strip().lower()]

                if field[0] in self.db.fields_names and field[0] not in self.status and (field[0] != 'is_healthy'):
                    if 'field' in self.status:
                        self.context.payload.update('field', field[0])
                    else:
                        self.context.payload.insert('field', field[0])

                    list_param = {x: x for x in self.db.values[field[0]]}
                    choice = [True if len(list_param) > 10 else False]
                    self.context.add_bot_msgs([Utils.chat_message(f"Please provide a {field[0]}"),
                                               Utils.choice(field[0], list_param, show_search=choice)])
                    return ValueAction(self.context), False

                elif field[0] in self.db.fields_names and (field[0] != 'is_healthy'):
                    if 'field' in self.status:
                        self.context.payload.update('field', field[0])
                    else:
                        self.context.payload.insert('field', field[0])
                    list_param = {x: x for x in self.db.values[field[0]]}
                    choice = [True if len(list_param) > 10 else False]

                    self.context.add_bot_msgs(
                        [Utils.chat_message(f"Do you want to change the {field[0]} or add a new {field[0]}?"),
                         Utils.choice(field[0], list_param, show_search=choice)])
                    return ChangeAddAction(self.context), False

                elif (field[0] == 'is_healthy'):
                    if 'field' in self.status:
                        self.context.payload.update('field', field[0])
                    else:
                        self.context.payload.insert('field', field[0])
                    self.context.add_bot_msgs([Utils.chat_message(messages.healthy_patients),
                                               Utils.choice(field[0], {'Yes': 'yes', 'No': 'no'})])
                    return ValueAction(self.context), False

                else:
                    list_param = {x: x for x in self.db.fields_names}
                    self.context.add_bot_msgs([Utils.chat_message(messages.wrong_choice),
                                               Utils.choice('Available fields', list_param)])
                    return None, False

            fields = {x: self.status[x] for x in self.db.fields if x in self.status}

            self.context.payload.clear()
            self.context.payload.insert('fields', fields)
            self.context.add_bot_msgs(
                [Utils.param_list(fields), Utils.tools_setup(add=None, remove=['available_choices']),
                 Utils.tools_setup(add=None, remove=['table']), Utils.tools_setup(add=None, remove=['data_summary'])])
            return DSNameAction(self.context), True
        else:
            self.context.payload.clear()
            self.db.go_back({})
            self.context.add_bot_msgs([Utils.chat_message(messages.no_exp_found)])
            self.context.add_bot_msgs([Utils.chat_message("Which field do you want to select?")])
            return None, False
