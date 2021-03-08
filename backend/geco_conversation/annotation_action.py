from data_structure.database import annotation_fields
from geco_conversation import *
from geco_utilities import messages, helpMessages


class AnnotationAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.annotation_help)])
        return None, False

    def on_enter(self):
        node, bool = self.logic(None, None, None)
        return node, bool

    def check_status(self):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in self.db.fields:
                self.context.payload.replace(k, [x for x in v if
                                                 x in self.context.payload.database.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

    def filter(self, gcm_filter):
        if len(gcm_filter) > 0:
            self.db.update(gcm_filter)

        samples = self.db.check_existance(gcm_filter)

        return samples

    def logic(self, message, intent, entities):
        from .value_action import DSNameAction

        self.context.payload.back = AnnotationAction
        self.check_status()
        gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields}
        samples = self.filter(gcm_filter)

        missing_fields = self.db.fields_names
        list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
        #self.context.add_bot_msgs([Utils.table_viz('Table', self.db_table.drop('local_url', axis=1))])
        if samples > 0:
            if len(list_param) != 0:
                if gcm_filter != {}:
                    self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                                               Utils.choice('Available fields', list_param, show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list({k: v for (k, v) in self.status.items() if
                                                                 k in self.context.database.fields})] + Utils.create_piecharts(
                        self.context, gcm_filter))
                    return FieldAction(self.context), False
                else:
                    self.context.add_bot_msgs([Utils.chat_message(messages.choice_field),
                                               Utils.choice('Available fields', list_param, show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list({k: v for (k, v) in self.status.items() if
                                                                 k in self.db.fields})] + Utils.create_piecharts(
                        self.context, gcm_filter))
                    return FieldAction(self.context), False
            else:
                fields = {x: self.status[x] for x in self.db.fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs(
                    [Utils.param_list(fields), Utils.tools_setup(add=None, remove='available_choices'),
                     Utils.tools_setup(add=None, remove='table')])
                return DSNameAction(self.context), True

        else:
            for x in annotation_fields:
                if x in self.status:
                    self.context.payload.delete(x)
            self.db.go_back({})
            self.context.add_bot_msgs([Utils.chat_message(messages.no_exp_found)])
            return None, False
