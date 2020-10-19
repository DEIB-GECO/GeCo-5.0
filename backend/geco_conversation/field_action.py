from data_structure.database import experiment_fields, annotation_fields
from geco_conversation import *

class FieldAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.fields_help)]

    def logic(self, message, intent, entities):
        from .confirm import AskConfirm
        from .annotation_action import AnnotationAction
        from .experiment_action import ExperimentAction
        from .value_action import ValueAction
        from .change_add_action import ChangeAddAction

        if self.context.payload.back == AnnotationAction:
            available_fields = annotation_fields
        elif self.context.payload.back == ExperimentAction:
            available_fields = experiment_fields

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in available_fields:
                self.context.payload.replace(k, [x for x in v if
                                                 x in getattr(self.context.payload.database, str(k) + '_db')])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)
            else:
                self.context.payload.delete(k)

        if intent != 'deny':
            missing_fields = list(set(self.context.payload.database.fields_names).difference(set(self.status.keys())))
            field = entities['field'] if 'field' in entities else [message.strip().lower()]

            if field[0] in missing_fields and (field[0] != 'is_healthy'):
                if 'field' in self.status:
                    #old = self.status['field'].copy()
                    #self.status['field'].append(field[0])
                    self.context.payload.update('field', field[0])
                else:
                    self.context.payload.insert('field', field[0])
                    #self.context.top_delta().insert_value('field')
                    #self.status['field'] = [field[0]]

                list_param = {x: x for x in getattr(self.context.payload.database, str(field[0]) + '_db')}
                choice = [True if len(list_param) > 10 else False]
                self.context.add_bot_msgs([Utils.chat_message("Please provide a {}".format(field[0])),
                        Utils.choice(field[0], list_param, show_search=choice)])
                return ValueAction(self.context), False

            elif field[0] in self.context.payload.database.fields_names and (field[0] != 'is_healthy'):
                if 'field' in self.status:
                    self.context.payload.update('field', field[0])
                else:
                    self.context.payload.insert('field', field[0])
                list_param = {x: x for x in getattr(self.context.payload.database, str(field[0]) + '_db')}
                choice = [True if len(list_param) > 10 else False]

                self.context.add_bot_msgs([Utils.chat_message("Do you want to change the {} or add a new {}?".format(field[0], field[0])),
                        Utils.choice(field[0], list_param, show_search=choice)])
                return ChangeAddAction(self.context), False

            elif (field[0] == 'is_healthy'):
                if 'field' in self.status:
                    self.context.payload.update('field', field[0])
                else:
                    self.context.payload.insert('field', field[0])
                self.context.add_bot_msgs([Utils.chat_message(messages.healthy_patients)])
                return ValueAction(self.context), False

            else:
                list_param = {x: x for x in missing_fields}
                self.context.add_bot_msgs([Utils.chat_message(messages.wrong_choice),
                        Utils.choice('Available fields', list_param)])
                return None, False

        fields = {x: self.status[x] for x in available_fields if x in self.status}
        self.context.payload.clear()
        self.context.payload.insert('fields', fields)
        self.context.add_bot_msgs([Utils.param_list(self.status['fields'])])
        return AskConfirm(self.context), True


