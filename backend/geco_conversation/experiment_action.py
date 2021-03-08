from data_structure.database import experiment_fields
from geco_conversation import *


class ExperimentAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.experiment_help)])
        return None, False

    def on_enter(self):
        node, bool = self.logic(None, None, None)
        return node, bool

    def is_healthy(self):
        if 'is_healthy' in self.status:
            if self.status['is_healthy'] == ['healthy']:
                self.context.payload.insert('is_healthy', ['true'])
            if self.status['is_healthy'] == ['tumoral']:
                self.context.payload.insert('is_healthy', ['false'])

    def check_status(self):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in self.db.fields:
                self.context.payload.replace(k, list(set([x for x in v if x in self.db.values[k]])))
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)
            else:
                self.context.payload.delete(k)

    def filter(self, gcm_filter):
        if len(gcm_filter) > 0:
            self.db.update(gcm_filter)

        samples = self.db.check_existance(gcm_filter)

        return samples

    def logic(self, message, intent, entities):
        from .value_action import DSNameAction

        self.context.payload.back = ExperimentAction
        self.is_healthy()
        self.check_status()
        gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields}
        samples = self.filter(gcm_filter)

        # Find fields that are not already selected by the user
        missing_fields = self.db.fields_names

        self.context.add_bot_msgs([Utils.table_viz('Table', self.db_table.drop('local_url', axis=1))])
        if samples > 0:
            list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}

            if len(list_param) != 0:
                if gcm_filter != {}:
                    self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                                               Utils.choice('Available fields', list_param, show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list(gcm_filter)] +
                                              Utils.create_piecharts(self.context, gcm_filter))
                    return FieldAction(self.context), False
                else:
                    self.context.add_bot_msgs([Utils.chat_message(messages.choice_field),
                                               Utils.choice('Available fields', list_param, show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list(gcm_filter)] +
                                              Utils.create_piecharts(self.context, gcm_filter))
                    return FieldAction(self.context), False
            else:
                fields = {x: self.status[x] for x in experiment_fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs([Utils.param_list(fields),Utils.tools_setup(add=None, remove='available_choices'),
                     Utils.tools_setup(add=None, remove='table'),Utils.tools_setup(add=None, remove='data_summary')])
                return DSNameAction(self.context), True

        else:
            for x in experiment_fields:
                if x in self.status:
                    self.context.payload.delete(x)

            fields = {x: self.status[x] for x in experiment_fields if x in self.status}
            self.db.go_back({})
            self.context.add_bot_msgs([Utils.param_list(fields), Utils.chat_message(messages.no_exp_found)])
            list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
            self.context.add_bot_msgs([Utils.chat_message(messages.choice_field),
                                       Utils.choice('Available fields', list_param, show_help=True,
                                                    helpIconContent=helpMessages.fields_help),
                                       Utils.param_list(
                                           {k: v for (k, v) in self.status.items() if k in experiment_fields})] +
                                      Utils.create_piecharts(self.context, gcm_filter))
            return FieldAction(self.context), False
