from database import experiment_fields
from geco_conversation import *

class ExperimentAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.experiment_help)])
        return None, False

    def logic(self, message, intent, entities):
        from .askconfirm import AskConfirm
        from .field_action import FieldAction

        self.context.payload.back = ExperimentAction

        if 'is_healthy' in self.status:
            if self.status['is_healthy']== ['healthy']:
                self.status['is_healthy'] = [True]
                self.context.top_delta().insert_value('is_healthy')
            if self.status['is_healthy'] == ['tumoral']:
                self.status['is_healthy'] = [False]
                self.context.top_delta().insert_value('is_healthy')

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in experiment_fields:
                self.status[k] = [x for x in v if x in getattr(self.context.payload.database, str(k) + '_db')]
                if len(self.status[k]) == 0:
                    del (self.status[k])

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
                    self.status.clear()
                    self.status['fields'] = fields
                    self.context.add_bot_msgs([Utils.param_list(self.status['fields'])])
                    return AskConfirm(self.context), True
        else:
            for x in experiment_fields:
                if x in self.status:
                    del self.status[x]
            self.context.add_bot_msgs([Utils.param_list(fields), Utils.chat_message(messages.no_exp_found)])
            return None, False


