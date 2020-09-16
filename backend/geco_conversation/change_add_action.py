from database import experiment_fields, annotation_fields
import messages
from geco_conversation import *

class ChangeAddAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.experiment_help)]

    def required_additional_status(self):
        return ['geno_surf']

    def create_piecharts(self, gcm_filter):
        msgs = []
        msgs.append(Utils.tools_setup('dataviz','dataset'))
        values = {k:v for (k,v) in list(
            sorted(
                [(x, self.context.payload.database.retrieve_values(gcm_filter, x)) for x in self.context.payload.database.fields_names if x not in self.status and x!='is_healthy'],
                key = lambda x : len(x[1])))[:6]}

        msgs.append(Utils.pie_chart(values))
        return msgs

    def logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status.items() if k in experiment_fields}

        if len(gcm_filter) > 0:
            self.context.payload.database.update(gcm_filter)

        if intent == 'change_option':
            self.status[self.status['field']] = []
            self.context.top_delta().delete_value(self.status['field'], self.status[self.status['field']])

            return ValueAction(self.context), False

        elif intent == 'add_option':

            list_param = {x: x for x in getattr(self.context.payload.database, str(self.status['field'] + '_db'))}
            choice = [True if len(list_param) > 10 else False]

            self.context.add_bot_msgs([Utils.chat_message("Please provide a {}".format(self.status['field'])),
                    Utils.choice(self.status['field'], list_param, show_search=choice)])
            return ValueAction(self.context), False
        else:
            list_param = {x: x for x in self.context.payload.database.fields_names}
            # self.logic = self.field_logic
            self.context.add_bot_msgs([Utils.chat_message("Sorry, I didn't understand. Do you want to change or add a new {}?".format(self.status['field'])),Utils.choice('Available fields', list_param)])
            return None, False

        fields = {x: self.status[x] for x in experiment_fields if x in self.status}
        self.status.clear()
        self.status['fields'] = fields
        self.status['back'] = ExperimentAction
        self.context.add_bot_msgs([Utils.param_list({k: v for (k, v) in self.status.items() if k in experiment_fields})])
        return Confirm(self.context), False



