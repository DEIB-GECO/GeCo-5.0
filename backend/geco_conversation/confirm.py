from data_structure.data_structure import DataSet
from geco_conversation import *

class AskConfirm(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.confirm_help)]

    def logic(self, message, intent, entities):

        if message is None:
            list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
            if 'metadata' in self.status['fields']:
                list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                               self.status['fields']['metadata']})
            self.context.add_bot_msgs([Utils.chat_message(messages.confirm_selection), Utils.param_list(list_param)])
            return Confirm(self.context), False

class Confirm(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.confirm_help)]

    def logic(self, message, intent, entities):
        if self.context.payload.back!= MetadataAction:
            if intent == "affirm":
                self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
                return RenameAction(self.context), False
            else:
                self.context.add_bot_msgs([Utils.chat_message(messages.restart_selection)])
                return ChangeSelectionAction(self.context), False
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

                self.context.add_bot_msgs([Utils.chat_message(messages.download), Utils.param_list(list_param),Utils.workflow('Data selection', True, urls)])
                return GmqlAction(self.context), True

class RenameAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.rename_help)]

    def logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )

        urls = self.context.payload.database.download(self.status['fields'])

        #ds = DataSet(self.status['fields'], name)
        #self.context.data_extraction.datasets.append(ds)
        self.status['fields'].update({'name':name})
        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        self.context.add_bot_msgs([Utils.chat_message("OK, dataset saved with name: " + name),Utils.chat_message(messages.download),
                Utils.param_list(list_param), Utils.workflow('Data selection', True, urls)])
        return FilterMetadataAction(self.context), True

class ChangeSelectionAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_selection_help)]

    def logic(self, message, intent, entities):
        if intent == "affirm":
            from .start_action import StartAction
            return StartAction({}), True
        else:
            list_param = {x: x for x in self.status['fields']}
            self.context.add_bot_msgs([Utils.chat_message(messages.change_field),
                    Utils.choice("Fields selected", list_param)])
            return ChangeFieldAction(self.context), False

class ChangeFieldAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(helpMessages.change_field_help)]

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

