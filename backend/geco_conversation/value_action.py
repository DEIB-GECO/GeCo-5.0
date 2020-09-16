from database import experiment_fields, annotation_fields
import messages
from geco_conversation import *

class ValueAction(AbstractAction):

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
        from .confirm import Confirm
        if self.context.payload.back == AnnotationAction:
            available_fields = annotation_fields
        elif self.context.payload.back == ExperimentAction:
            available_fields = experiment_fields

        request_field = self.status['field']

        db = getattr(self.context.payload.database, request_field + '_db')
        given_value = entities[request_field] if ((request_field in entities) and (any(elem in db for elem in entities[request_field]))) else [message.strip().lower()]
        if request_field == 'is_healthy':
            if intent == 'affirm':
                self.status[request_field] = ['true']
            else:
                self.status[request_field] = ['false']

            self.context.top_delta().insert_value(request_field)
            gcm_filter = {k: v for (k, v) in self.status.items() if k in available_fields}
            list_param = {x: x for x in self.context.payload.database.fields_names}
            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)
            pie_charts = self.create_piecharts(gcm_filter)

            self.context.add_bot_msgs([Utils.chat_message("Do you want to filter more? If so, which one do you want to select now?"),
                    Utils.choice('Available fields', list_param),
                    Utils.param_list({k: v for (k, v) in self.status.items() if k in available_fields})] + \
                   pie_charts)
            return FieldAction(self.context), False

        elif any(elem in db for elem in given_value):
            for i in range(len(given_value)):
                if given_value[i] in db:
                    if request_field in self.status:
                        if given_value[i] not in self.status[request_field]:
                            self.context.top_delta().update_value(request_field, self.status[request_field],
                                                              self.status[request_field].append(given_value[i]))
                            self.status[request_field].append(given_value[i])
                    else:
                        self.context.top_delta().insert_value(request_field)
                        self.status[request_field] = [given_value[i]]

            gcm_filter = {k: v for (k, v) in self.status.items() if k in available_fields}
            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)
            list_param = {x: x for x in self.context.payload.database.fields_names}
            pie_charts = self.create_piecharts(gcm_filter)
            print('**************************')
            print(self.status.items())
            if len(list_param) > 0:

                self.context.add_bot_msgs([Utils.chat_message("Do you want to filter more? If so, which one do you want to select now?"),
                        Utils.choice('Available fields', list_param), Utils.param_list(
                        {k: v for (k, v) in self.status.items() if k in available_fields})] + pie_charts)
                return FieldAction(self.context), False
            else:
                from .confirm import Confirm
                fields = {x: self.status[x] for x in available_fields if x in self.status}
                self.status.clear()
                self.status['fields'] = fields
                print(self.status)
                self.context.add_bot_msgs([Utils.param_list(self.status['fields'])])
                return Confirm(self.context), True

        else:

            list_param = {x: x for x in getattr(self.context.payload.database, str(request_field) + '_db')}
            choice = [True if len(list_param) > 10 else False]
            self.context.add_bot_msgs([Utils.chat_message("The {} {} not valid, insert a valid one".format(request_field, given_value)),
                    Utils.choice(request_field, list_param, show_search=choice)])
            return None, False