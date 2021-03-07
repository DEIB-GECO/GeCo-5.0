from data_structure.dataset import Dataset
from geco_conversation import *


class Confirm(AbstractDBAction):
    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.confirm_help)])
        return None, True

    def on_enter(self):
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        if 'metadata' in self.status['fields']:
            list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                               self.status['fields']['metadata']})
        self.context.add_bot_msgs([Utils.chat_message(messages.confirm_selection), Utils.param_list(list_param)])
        return None, False

    def logic(self, message, intent, entities):
        if self.context.payload.back != RegionAction:
            return DSNameAction(self.context), True
            # if intent == "affirm":
            #    self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
            #   return RenameAction(self.context, MetadataAction(self.context)), False
            # else:
            #   self.context.add_bot_msgs([Utils.chat_message(messages.restart_selection)])
            #   return ChangeSelection(self.context), False
        else:
            if intent == "affirm":
                fields = self.status['fields'].copy()
                if 'metadata' in fields:
                    del (fields['metadata'])
                if 'name' in fields:
                    del (fields['name'])

                links = self.db.download(fields)
                # urls = []
                list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
                meta_dict = {}
                if 'metadata' in self.status:
                    for x in self.status['metadata']:
                        meta_dict[x] = self.status["metadata"][x]
                meta = {'metadata': meta_dict}
                donors = self.db.retrieve_donors(meta['metadata'])
                self.context.payload.insert('donors', donors)
                # print(self.status['donors'])
                if meta_dict != {}:
                    list_param.update(meta)
                list_param_ds = list_param.copy()
                name = list_param['name']
                del (list_param_ds['name'])
                dict_for_join = {i: {'donor': d, 'is_healthy': h, 'disease': dis}
                                 for i, d, h, dis in
                                 self.db_table[['item_id', 'donor_source_id', 'is_healthy', 'disease']].values}
                ds = Dataset(list_param_ds, name, donors=self.status['donors'],
                             items=list(set(self.db_table['item_id'])))
                ds.dict_for_join = dict_for_join
                self.context.data_extraction.datasets.append(ds)

                self.db.go_back({})
                # fields =  {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata' and x!='name'}
                # print(fields)
                # print(self.status['fields']['metadata'])
                # meta = self.context.payload.database.retrieve_meta(fields,self.status['fields']['metadata'])
                # ds.add_meta_table(meta)
                if len(meta_dict.keys()) > 0:
                    self.context.workflow.add(Select(ds, metadata=meta_dict))
                else:
                    self.context.workflow.add(Select(ds))
                self.context.add_bot_msgs([Utils.chat_message(messages.download),
                                           Utils.workflow('Data Selection', download=True, link_list=links),
                                           Utils.param_list(list_param),
                                           Utils.tools_setup(add=None, remove='data_summary')])

                # self.context.add_bot_msgs([Utils.chat_message(messages.download),Utils.workflow('Data Selection',download=True,link_list=links), Utils.chat_message(messages.gmql_operations), Utils.param_list(list_param), Utils.tools_setup(add=None,remove='data_summary')])
                # if len(self.context.data_extraction.datasets)%2==0:
                #    return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
                # else:
                #   return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
                return PivotAction(self.context), True
            else:
                self.context.add_bot_msgs(
                    [Utils.chat_message('Do you want to restart your selection from scratch?')])
                return ChangeSelection(self.context), False


class ChangeSelection(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_selection_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent == "affirm":
            from .start_action import StartAction
            return StartAction({}), True
        else:
            list_param = {x: x for x in self.status['fields']}
            self.context.add_bot_msgs([Utils.chat_message(messages.change_field),
                                       Utils.choice("Fields selected", list_param)])
            return ChangeField(self.context), False


class ChangeField(AbstractDBAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_field_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        selected_field = message.strip().lower()

        if selected_field in self.status['fields'] and selected_field != 'metadata':
            # self.context.payload.delete(self.status['field'])
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if
                          k in self.db.fields and k != selected_field and k != 'metadata'}
            self.context.payload.delete_from_dict('fields',selected_field)
            if len(gcm_filter) > 0:
                self.db.go_back(gcm_filter)

            list_param = {x: x for x in self.db.values[selected_field]}
            # fields = {k:v for (k,v) in self.status['fields'].items() if k != selected_field}

            # self.context.payload.delete(self.status['field'])
            self.context.add_bot_msgs(
                [Utils.chat_message("Which value do you want?"), Utils.choice(str(selected_field), list_param)])
            return ValueAction(self.context), False
            # return self.status['back'](self.context), True
        elif selected_field == 'metadata' or selected_field in self.status['fields']['metadata']:
            from .metadata_action import KeyAction
            if selected_field == 'metadata':
                list_param = {x: x for x in self.status['fields']['metadata']}
                if list_param.keys() == 1:
                    self.context.add_bot_msgs([Utils.chat_message('Which one do you want to change?'),
                                               Utils.choice("Metadata selected", list_param)])
                    return ChangeMetadata(self.context), False
                else:
                    selected_field = list_param.keys()[0]
                    # gcm_filter = {k: v for (k, v) in self.status['field'].items() if k in self.context.payload.database.fields and k != selected_field  and k!='metadata'}

                    # if len(gcm_filter) > 0:
                    #   self.context.payload.database.go_back(gcm_filter)
                    self.context.payload.delete(selected_field, self.status['fields']['metadata'][selected_field])
                    list_param = {x: x for x in list(
                        set(self.db.metadata[self.db.metadata['key'] == selected_field]['values'].values))}
                    self.context.add_bot_msgs(
                        [Utils.chat_message("Which value do you want?"), Utils.choice(str(selected_field), list_param)])
                    return KeyAction(self.context), False
            else:
                self.context.payload.delete(selected_field, self.status['fields']['metadata'][selected_field])
                list_param = {x: x for x in list(set(self.db.metadata[
                                                         self.db.metadata[
                                                             'key'] == selected_field]['values'].values))}

                self.context.add_bot_msgs(
                    [Utils.chat_message("Which value do you want?"), Utils.choice(str(selected_field), list_param)])
                return KeyAction(self.context), False

        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.wrong_field)])
            return None, False


class ChangeMetadata(AbstractDBAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_field_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from .metadata_action import KeyAction
        selected_field = message.strip().lower()

        if selected_field in self.status['fields']['metadata']:
            self.context.payload.delete(selected_field, self.status['fields']['metadata'][selected_field])
            list_param = {x: x for x in list(set(self.db.metadata[
                                                     self.db.metadata[
                                                         'key'] == selected_field]['values'].values))}

            self.context.add_bot_msgs(
                [Utils.chat_message("Which value do you want?"), Utils.choice(str(selected_field), list_param)])
            return KeyAction(self.context), False
