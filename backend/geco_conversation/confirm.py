from data_structure.dataset import Dataset
from geco_conversation import *

class Confirm(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.confirm_help)]

    def on_enter(self):
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        if 'metadata' in self.status['fields']:
            list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                               self.status['fields']['metadata']})
        self.context.add_bot_msgs([Utils.chat_message(messages.confirm_selection), Utils.param_list(list_param)])
        return None, False

    def logic(self, message, intent, entities):
        if self.context.payload.back!= RegionAction:
            return DSNameAction(self.context), True
            #if intent == "affirm":
            #    self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
             #   return RenameAction(self.context, MetadataAction(self.context)), False
            #else:
             #   self.context.add_bot_msgs([Utils.chat_message(messages.restart_selection)])
             #   return ChangeSelection(self.context), False
        else:
            if intent == "affirm":
                fields = self.status['fields'].copy()
                if 'metadata' in fields:
                    del(fields['metadata'])
                del(fields['name'])
                #urls = self.context.payload.database.download_filter_meta(fields,self.status['fields']['metadata'])
                #urls = []
                list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
                list_param.update({'metadata': '{}: {}'.format(x, self.status['metadata'][x]) for x in
                                   self.status['metadata']})
                list_param_ds = list_param.copy()
                name = list_param['name']
                del(list_param_ds['name'])
                ds = Dataset(list_param_ds, name)
                self.context.data_extraction.datasets.append(ds)
                #fields =  {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata' and x!='name'}
                #print(fields)
                #print(self.status['fields']['metadata'])
                #meta = self.context.payload.database.retrieve_meta(fields,self.status['fields']['metadata'])
                #ds.add_meta_table(meta)
                if len(self.status['metadata'].keys())>0:
                    self.context.workflow.add(Select(ds, metadata=self.status['metadata']))
                else:
                    self.context.workflow.add(Select(ds))
                self.context.add_bot_msgs([Utils.chat_message(messages.download), Utils.chat_message(messages.gmql_operations), Utils.param_list(list_param)])
                if len(self.context.data_extraction.datasets)%2==0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
                else:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False


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

class ChangeField(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_field_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        selected_field = message.strip().lower()

        if selected_field in self.status['fields']:
            self.context.payload.delete(self.status['field'])
            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}

            if len(gcm_filter) > 0:
                self.context.payload.database.update(gcm_filter)

            list_param = {x: x for x in self.context.payload.database.values[selected_field]}
            #fields = {k:v for (k,v) in self.status['fields'].items() if k != selected_field}

            self.context.add_bot_msgs([Utils.chat_message("Which value do you want?"),Utils.choice(str(selected_field), list_param)])
            return ValueAction(self.context), False
            #return self.status['back'](self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.wrong_field)])
            return None, False


