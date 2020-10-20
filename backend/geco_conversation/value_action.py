from data_structure.database import experiment_fields, annotation_fields
from geco_conversation import *

class ValueAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.value_help)]

    def logic(self, message, intent, entities):
        if self.context.payload.back == AnnotationAction:
            available_fields = annotation_fields
        elif self.context.payload.back == ExperimentAction:
            available_fields = experiment_fields

        request_field = self.status['field'][-1]
        db = getattr(self.context.payload.database, request_field + '_db')
        given_value = entities[request_field] if ((request_field in entities) and (any(elem in db for elem in entities[request_field]))) else [message.strip().lower()]

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in available_fields:
                self.context.payload.replace(k, [x for x in v if
                                                 x in getattr(self.context.payload.database, str(k) + '_db')])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

        if request_field == 'is_healthy':
            if intent == 'affirm':
                #self.status[request_field] = ['true']
                self.context.payload.insert('is_healthy', ['true'])
            else:
                #self.status[request_field] = ['false']
                self.context.payload.insert('is_healthy', ['false'])


            gcm_filter = {k: v for (k, v) in self.status.items() if (k in available_fields)}
            list_param = {x: x for x in self.context.payload.database.fields_names}

            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)

            self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                    Utils.choice('Available fields', list_param),
                    Utils.param_list({k: v for (k, v) in self.status.items() if k in available_fields})] + \
                   Utils.create_piecharts(self.context,gcm_filter))
            return FieldAction(self.context), False

        elif any(elem in db for elem in given_value):
            for i in range(len(given_value)):
                if given_value[i] in db:
                    if request_field in self.status:
                        if given_value[i] not in self.status[request_field]:
                            #self.context.top_delta().update_value(request_field, self.status[request_field],
                                                             # self.status[request_field].append(given_value[i]))
                            self.context.payload.update(request_field,given_value[i])
                            #self.status[request_field].append(given_value[i])
                    else:
                        self.context.payload.insert(request_field, [given_value[i]])

            gcm_filter = {k: v for (k, v) in self.status.items() if k in available_fields}
            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)
            list_param = {x: x for x in self.context.payload.database.fields_names}

            if len(list_param) > 0:
                self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                        Utils.choice('Available fields', list_param), Utils.param_list(
                        {k: v for (k, v) in self.status.items() if (k in available_fields) and (any(elem in db for elem in v))})] + Utils.create_piecharts(self.context,gcm_filter))
                return FieldAction(self.context), False
            else:
                from .confirm import AskConfirm
                fields = {x: self.status[x] for x in available_fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs([Utils.param_list(fields)])
                return AskConfirm(self.context), True

        else:
            list_param = {x: x for x in getattr(self.context.payload.database, str(request_field) + '_db')}
            choice = [True if len(list_param) > 10 else False]
            self.context.add_bot_msgs([Utils.chat_message("The {} {} not valid, insert a valid one".format(request_field, given_value)),
                    Utils.choice(request_field, list_param, show_search=choice)])
            return None, False