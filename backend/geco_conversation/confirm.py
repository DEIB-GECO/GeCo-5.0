from data_structure.datastructures import DataSet
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
        if self.context.payload.back!= MetadataAction:
            if intent == "affirm":
                self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
                return Rename(self.context), False
            else:
                self.context.add_bot_msgs([Utils.chat_message(messages.restart_selection)])
                return ChangeSelection(self.context), False
        else:
            if intent == "affirm":
                fields = self.status['fields'].copy()
                del(fields['metadata'])
                del(fields['name'])
                urls = self.context.payload.database.download_filter_meta(fields,self.status['fields']['metadata'])
                list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
                list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                                   self.status['fields']['metadata']})
                list_param_ds = list_param.copy()
                name = list_param['name']
                del(list_param_ds['name'])
                ds = DataSet(list_param_ds, name)
                self.context.data_extraction.datasets.append(ds)
                self.context.workflow.add_gmql('select', {'Dataset':ds})
                self.context.add_bot_msgs([Utils.chat_message(messages.download), Utils.chat_message(messages.gmql_operations), Utils.param_list(list_param),Utils.workflow('Data selection', True, urls)])
                if len(self.context.data_extraction.datasets)%2==0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
                else:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

class Rename(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.rename_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )

        urls = self.context.payload.database.download(self.status['fields'])

        #ds = DataSet(self.status['fields'], name)
        #self.context.data_extraction.datasets.append(ds)
        self.context.payload.update('fields', {'name':name})
        #self.status['fields'].update({'name':name})
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        self.context.add_bot_msgs([Utils.chat_message("OK, dataset saved with name: " + name),Utils.chat_message(messages.download),
                Utils.param_list(list_param), Utils.workflow('Data selection', True, urls)])
        return FilterMetadata(self.context), True

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
            list_param = {x: x for x in getattr(self.context.payload.database, str(selected_field) + '_db')}
            fields = {k:v for (k,v) in self.status['fields'].items() if k != selected_field}
            self.context.add_bot_msgs([Utils.choice(str(selected_field), list_param)])
            return self.status['back'](self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.wrong_field)])
            return None, False


class NewDataset(AbstractAction):
    def help_message(self):
        return []

    def on_enter(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])

    def logic(self, message, intent, entities):
        if intent=='affirm':
            return StartAction(self.context), True
        elif intent=='deny':
            return PivotAction(self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.not_understood)])
            return None, False