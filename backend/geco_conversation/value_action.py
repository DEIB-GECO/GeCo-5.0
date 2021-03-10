from data_structure.database import experiment_fields, annotation_fields
from geco_conversation import *


class ValueAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.value_help)])
        return None, False

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):

        request_field = self.status['field'][-1]
        print('gfields', self.status['field'])
        print('req_field', request_field)
        db = self.db.values[request_field]
        given_value = entities[request_field] if (
                (request_field in entities) and (any(elem in db for elem in entities[request_field]))) else [
            message.strip().lower()]
        print('given_val', given_value)
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in self.db.fields and k != 'is_healthy':
                self.context.payload.replace(k, [x for x in v if
                                                 x in self.db.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

        if request_field == 'is_healthy':
            if intent == 'affirm':
                self.context.payload.insert('is_healthy', [True])
            else:
                self.context.payload.insert('is_healthy', [False])

            gcm_filter = {k: v for (k, v) in self.status.items() if (k in self.db.fields)}

            if len(gcm_filter) > 0:
                self.cdb.update(gcm_filter)
                list_param = {k: v for (k, v) in self.status.items() if k in self.db.fields_names}
                choices = {x: x for x in self.db.fields_names}
            self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                                       Utils.choice('Available fields', choices),
                                       Utils.param_list(list_param)] + \
                                      Utils.create_piecharts(self.context, gcm_filter))
            #self.context.add_bot_msgs([Utils.table_viz('Table', self.db_table.drop('local_url', axis=1))])
            return FieldAction(self.context), False

        elif any(elem in db for elem in given_value):
            for i in range(len(given_value)):
                if given_value[i] in db:
                    if request_field in self.status:
                        if given_value[i] not in self.status[request_field]:
                            self.context.payload.update(request_field, given_value[i])
                    else:
                        self.context.payload.insert(request_field, [given_value[i]])

            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.db.fields}
            if len(gcm_filter) > 0:
                self.db.update(gcm_filter)
            choice = {x: x for x in self.db.fields_names}
            list_param = {k: v for (k, v) in self.status.items() if (k in self.db.fields)}
            if len(choice) > 0:
                self.context.add_bot_msgs([Utils.chat_message(messages.filter_more),
                                           Utils.choice('Available fields', choice),
                                           Utils.param_list(list_param)] + Utils.create_piecharts(self.context,
                                                                                                  gcm_filter))
                #self.context.add_bot_msgs([Utils.table_viz('Table', self.db_table.drop('local_url', axis=1))])
                return FieldAction(self.context), False
            else:

                from .confirm import Confirm
                fields = {x: self.status[x] for x in self.db.fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs([Utils.param_list(fields)])
                return DSNameAction(self.context), True

        else:

            list_param = {x: x for x in self.db.values[request_field]}
            choice = [True if len(list_param) > 10 else False]
            self.context.add_bot_msgs(
                [Utils.chat_message(f"The {request_field} {given_value} not valid, insert a valid one"),
                 Utils.choice(request_field, list_param, show_search=choice)])

            return ValueAction(self.context), False


class DSNameAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.value_help)]

    def on_enter(self):
        if len(set(self.context.payload.database.table['dataset_name']))==1:
            fields = self.status['fields']
            fields.update({'dataset_name': list(set(self.context.payload.database.table['dataset_name']))})
            self.context.payload.clear()
            self.context.payload.insert('fields', fields)
            self.context.add_bot_msgs([Utils.param_list(fields)])
            return RenameAction(self.context, MetadataAction(self.context)), True
        else:
            self.context.add_bot_msgs([Utils.chat_message('Which dataset do you want among these?'),
                                       Utils.choice('Datasets', {i:i for i in list(set(self.context.payload.database.table['dataset_name']))})])

            return DSNameAction(self.context), False

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
            self.context.add_bot_msgs(
                [Utils.chat_message('Sorry, I didn\'t understand.\nWhich dataset do you want among these?'),
                 Utils.choice('Datasets',
                              {i: i for i in list(set(self.context.payload.database.table['dataset_name']))})])
            return DSNameAction(self.context), False
