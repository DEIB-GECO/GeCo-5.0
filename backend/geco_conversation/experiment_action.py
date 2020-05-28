from get_api import experiment_fields
import messages
import numpy as np
import time
from geco_conversation import *

class ExperimentAction(AbstractAction):

    def on_enter_messages(self):
        return self.logic(None, None, None)

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf']

    def create_piecharts(self, gcm_filter):
        msgs = []
        msgs.append(Utils.tools_setup('dataviz','dataset'))
        values = {k:v for (k,v) in list(
            sorted(
                [(x, self.status['geno_surf'].retrieve_values(gcm_filter, x)) for x in self.status['geno_surf'].fields_names if x not in self.status and x!='is_healthy'],
                key = lambda x : len(x[1])))[:6]}

        msgs.append(Utils.pie_chart(values))
        return msgs

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        if 'is_healthy' in self.status:
            if self.status['is_healthy']== ['healthy']:
                self.status['is_healthy'] = [True]
                print(self.status['is_healthy'])
            if self.status['is_healthy'] == ['tumoral']:
                self.status['is_healthy'] = [False]

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in experiment_fields:
                self.status[k] = [x for x in v if x in getattr(self.status['geno_surf'], str(k) + '_db')]
                if len(self.status[k]) == 0:
                    del (self.status[k])

        gcm_filter = {k:v for (k,v) in self.status.items() if k in experiment_fields}

        if len(gcm_filter) > 0:
            self.status['geno_surf'].update(gcm_filter)
        pie_charts = self.create_piecharts(gcm_filter)
        #Find fields that are not already selected by the user
        #missing_fields = list(set(self.status['geno_surf'].fields_names).difference(set(self.status.keys())))
        missing_fields = self.status['geno_surf'].fields_names
        if message is None:
            list_param = {x: x for x in missing_fields.difference(set(self.status.keys()))}
            if len(list_param)!=0:
                self.logic = self.field_logic
                return [Utils.chat_message("Which field do you want to select?"),
                        Utils.choice('Available fields',list_param, show_help=True, helpIconContent=messages.fields_help),
                        Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})] + pie_charts, \
                       None, {}
            else:
                fields = {x: self.status[x] for x in experiment_fields if x in self.status}
                back = ExperimentAction

                return [], Confirm({"fields": fields, "back": back}), {}

        return [], None, {}



    def value_logic(self, message, intent, entities):
        request_field = self.status['field']

        db = getattr(self.status["geno_surf"], request_field + '_db')
        given_value = entities[request_field] if (request_field in entities) else [message.strip().lower()]
        if request_field=='is_healthy':

            if intent == 'affirm':
                self.status[request_field] = ['true']
            else:
                self.status[request_field] = ['false']

            gcm_filter = {k: v for (k, v) in self.status.items() if k in experiment_fields}
            list_param = {x: x for x in self.status['geno_surf'].fields_names}
            if len(gcm_filter) > 0:
                self.status['geno_surf'].update(gcm_filter)
            pie_charts = self.create_piecharts(gcm_filter)
            self.logic = self.field_logic
            return [Utils.chat_message("Do you want to filter more? If so, which one do you want to select now?"),
                    Utils.choice('Available fields', list_param),Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})] + pie_charts, None, {}

        elif given_value[0] not in db or message not in db:

            list_param = {x: x for x in getattr(self.status['geno_surf'], str(request_field) + '_db')}

            choice = [True if len(list_param) > 10 else False]
            return [Utils.chat_message("The {} {} not valid, insert a valid one".format(request_field, given_value)),
                    Utils.choice(request_field, list_param, show_search=choice)], \
                   None, {}

        else:
            if request_field not in self.status or self.status[request_field]==[]:
                self.status[request_field] = given_value
            else:
                self.status[request_field].append(given_value)

            gcm_filter = {k: v for (k, v) in self.status.items() if k in experiment_fields}
            if len(gcm_filter) > 0:
                self.status['geno_surf'].update(gcm_filter)
            list_param = {x: x for x in self.status['geno_surf'].fields_names}
            pie_charts = self.create_piecharts(gcm_filter)
            if len(list_param) > 0:
                self.logic = self.field_logic
                return [Utils.chat_message("Do you want to filter more? If so, which one do you want to select now?"),
                        Utils.choice('Available fields',list_param),Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})] + pie_charts, None, {}
            else:
                from .confirm import Confirm
                fields = {x: self.status[x] for x in experiment_fields if x in self.status}
                back = ExperimentAction

                return [], Confirm({"fields": fields, "back": back}), {}

    def field_logic(self, message, intent, entities):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in experiment_fields:
                self.status[k] = [x for x in v if x in getattr(self.status['geno_surf'], str(k) + '_db')]
                if len(self.status[k]) == 0:
                    del (self.status[k])

        from .confirm import Confirm
        gcm_filter = {k:v for (k,v) in self.status.items() if k in experiment_fields}
        if len(gcm_filter) > 0:
            self.status['geno_surf'].update(gcm_filter)
        pie_charts = self.create_piecharts(gcm_filter)
        if intent!='deny':
            missing_fields = list(set(self.status['geno_surf'].fields_names).difference(set(self.status.keys())))


            field = entities['field'] if 'field' in entities else [message.strip().lower()]
            if field[0] in missing_fields and (field[0]!='is_healthy'):
                self.status['field']=field[0]
                list_param = {x: x for x in getattr(self.status['geno_surf'], str(field[0]) + '_db')}
                choice = [True if len(list_param)>10 else False]
                self.logic = self.value_logic
                return [Utils.chat_message("Please provide a {}".format(field[0])),
                        Utils.choice(field[0], list_param, show_search=choice)] + pie_charts, \
                       None, {}
            elif field[0] in self.status['geno_surf'].fields_names and (field[0]!='is_healthy'):
                self.status['field'] = field[0]
                list_param = {x: x for x in getattr(self.status['geno_surf'], str(field[0]) + '_db')}
                choice = [True if len(list_param) > 10 else False]
                self.logic = self.add_value_logic
                return [Utils.chat_message("Do you want to change the {} or add a new {}?".format(field[0], field[0])),
                        Utils.choice(field[0], list_param, show_search=choice)] + pie_charts, \
                       None, {}
            elif (field[0]=='is_healthy'):
                self.status['field'] = field[0]
                list_param = {x: x for x in getattr(self.status['geno_surf'], str(field[0]) + '_db')}
                self.logic = self.value_logic
                return [Utils.chat_message("Do you want healthy patients?"),
                        Utils.choice(field[0], list_param)] + pie_charts, \
                       None, {}
            else:
                list_param = {x: x for x in missing_fields}
                return [Utils.chat_message("Sorry, your choice is not available. Please reinsert one."),
                        Utils.choice('Available fields', list_param)] + pie_charts, None, {}

        fields = {x:self.status[x] for x in experiment_fields if x in self.status}
        back = ExperimentAction

        return [], Confirm({"fields":fields, "back":back}), {}

    def add_value_logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status.items() if k in experiment_fields}
        print(gcm_filter)
        if len(gcm_filter) > 0:
            self.status['geno_surf'].update(gcm_filter)

        if intent == 'change_option':
            self.status[self.status['field']]=[]
            self.logic = self.value_logic
            return [], None, {}
        elif intent == 'add_option':
            #print(self.status)
            #missing_fields = list(set(self.status['geno_surf'].fields_names).difference(set(self.status.keys())))
            #list_param = {x: x for x in self.status['geno_surf'].fields_names}
            list_param = {x: x for x in getattr(self.status['geno_surf'], str(self.status['field'] + '_db'))}
            choice = [True if len(list_param) > 10 else False]
            self.logic = self.value_logic
            return [Utils.chat_message("Please provide a {}".format(self.status['field'])),
                    Utils.choice(self.status['field'], list_param, show_search=choice)], None, {}
        else:
            list_param = {x: x for x in self.status['geno_surf'].fields_names}
            self.logic = self.field_logic
            return [Utils.chat_message("Sorry, I didn't understand. Do you want to change or add a new {}?".format(self.status['field'])),
             Utils.choice('Available fields', list_param)], None, {}

        fields = {x: self.status[x] for x in experiment_fields if x in self.status}

        back = ExperimentAction

        return [], Confirm({"fields": fields, "back": back}), {}
