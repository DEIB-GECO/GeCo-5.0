from data_structure.database import experiment_fields, annotation_fields
from geco_conversation import *

class ValueAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.value_help)])
        return None, False

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):

        request_field = self.status['field'][-1]
        db = self.context.payload.database.values[request_field]
        given_value = entities[request_field] if ((request_field in entities) and (any(elem in db for elem in entities[request_field]))) else [message.strip().lower()]
        print('status_befare_value_action',self.status)
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in self.context.payload.database.fields and k!='is_healthy':
                self.context.payload.replace(k, [x for x in v if
                                                 x in self.context.payload.database.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

        if request_field == 'is_healthy':
            if intent == 'affirm':
                #self.status[request_field] = ['true']
                self.context.payload.insert('is_healthy', [True])
            else:
                #self.status[request_field] = ['false']
                self.context.payload.insert('is_healthy', [False])


            gcm_filter = {k: v for (k, v) in self.status.items() if (k in self.context.payload.database.fields)}

            print('###FIELDS####', self.context.payload.database.fields)
            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)
                print('table')
                print(self.context.payload.database.table.head())
                list_param = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields_names}
                choices = {x: x for x in self.context.payload.database.fields_names}
            self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                    Utils.choice('Available fields', choices),
                    Utils.param_list(list_param)] + \
                   Utils.create_piecharts(self.context,gcm_filter))
            self.context.add_bot_msgs([Utils.table_viz('Data Available', self.context.payload.database.table.drop('local_url',axis=1))])
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

            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
            print('gcm_value_action', gcm_filter)
            print('status_after_value_action', self.status)
            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)
            choice = {x: x for x in self.context.payload.database.fields_names}
            list_param = {k: v for (k, v) in self.status.items() if (k in self.context.payload.database.fields)}
            if len(choice) > 0:

                self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                        Utils.choice('Available fields', choice), Utils.param_list(list_param)] + Utils.create_piecharts(self.context,gcm_filter))
                self.context.add_bot_msgs([Utils.table_viz('Data Available', self.context.payload.database.table.drop('local_url',axis=1))])
                return FieldAction(self.context), False
            else:

                from .confirm import Confirm
                fields = {x: self.status[x] for x in self.context.payload.database.fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs([Utils.param_list(fields)])
                return DSNameAction(self.context), True
                #return RenameAction(self.context, MetadataAction(self.context)), True

        else:

            list_param = {x: x for x in self.context.payload.database.values[request_field]}
            choice = [True if len(list_param) > 10 else False]
            self.context.add_bot_msgs([Utils.chat_message("The {} {} not valid, insert a valid one".format(request_field, given_value)),
                    Utils.choice(request_field, list_param, show_search=choice)])

            return None, False

class DSNameAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.value_help)]

    def on_enter(self):
        if len(set(self.context.payload.database.table['dataset_name']))==1:
            fields = self.status['fields']
            fields.update({'dataset_name':list(set(self.context.payload.database.table['dataset_name']))})
            self.context.payload.clear()
            self.context.payload.insert('fields', fields)
            self.context.add_bot_msgs([Utils.param_list(fields)])
            return RenameAction(self.context, MetadataAction(self.context)), True
        else:
            self.context.add_bot_msgs([Utils.chat_message('Which dataset do you want among these?'),
                                       Utils.choice('Datasets', {i:i for i in list(set(self.context.payload.database.table['dataset_name']))})])

            return None, False

    def logic(self, message, intent, entities):
        if message in list(set(self.context.payload.database.table['dataset_name'])):
            ds_name = message
            fields = self.status['fields']
            fields.update({'dataset_name': ds_name})
            self.context.payload.clear()
            self.context.payload.insert('fields', fields)
            self.context.add_bot_msgs([Utils.param_list(fields)])
            return RenameAction(self.context, MetadataAction(self.context)), True
        else:
            self.context.add_bot_msgs([Utils.chat_message('Sorry, I didn\'t understand.\nWhich dataset do you want among these?'),
                                       Utils.choice('Datasets', {i:i for i in list(set(self.context.payload.database.table['dataset_name']))})])
            return None, False