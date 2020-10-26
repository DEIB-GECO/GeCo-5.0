from data_structure.database import experiment_fields
from geco_conversation import *

class ExperimentAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.experiment_help)])
        return None, False

    def on_enter(self):
        node, bool=self.logic(None,None,None)
        return node, bool

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        #from .field_action import FieldAction

        self.context.payload.back = ExperimentAction

        if 'is_healthy' in self.status:
            if self.status['is_healthy']== ['healthy']:
                self.context.payload.insert('is_healthy', ['true'])
            if self.status['is_healthy'] == ['tumoral']:
                self.context.payload.insert('is_healthy', ['false'])

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in experiment_fields:
                self.context.payload.replace(k, [x for x in v if x in self.context.payload.database.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

        gcm_filter = {k:v for (k,v) in self.status.items() if k in experiment_fields}

        if len(gcm_filter) > 0:
            self.context.payload.database.update(gcm_filter)
        #Find fields that are not already selected by the user
        #missing_fields = list(set(self.context.payload.database.fields_names).difference(set(self.status.keys())))
        missing_fields = self.context.payload.database.fields_names

        fields = {k: v for (k, v) in self.status.items() if k in experiment_fields}

        samples = self.context.payload.database.check_existance(fields)

        if samples > 0:
            if message is None:
                list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
                if len(list_param)!=0:
                    #print(self.logic)
                    self.context.add_bot_msgs([Utils.chat_message(messages.choice_field),
                                               Utils.choice('Available fields', list_param, show_help=True, helpIconContent=helpMessages.fields_help),
                                               Utils.param_list({k:v for (k, v) in self.status.items() if k in experiment_fields})]+
                                              Utils.create_piecharts(self.context,gcm_filter))
                    return FieldAction(self.context), False
                else:
                    fields = {x: self.status[x] for x in experiment_fields if x in self.status}
                    self.context.payload.clear()
                    self.context.payload.insert('fields', fields)
                    self.context.add_bot_msgs([Utils.param_list(fields)])
                    return Confirm(self.context), True
        else:
            for x in experiment_fields:
                if x in self.status:
                    self.context.payload.delete(x)
            self.context.add_bot_msgs([Utils.param_list(fields), Utils.chat_message(messages.no_exp_found)])
            list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
            self.context.add_bot_msgs([Utils.chat_message(messages.choice_field),
                                       Utils.choice('Available fields', list_param, show_help=True,
                                                    helpIconContent=helpMessages.fields_help),
                                       Utils.param_list(
                                           {k: v for (k, v) in self.status.items() if k in experiment_fields})] +
                                      Utils.create_piecharts(self.context, gcm_filter))
            return FieldAction(self.context), False


