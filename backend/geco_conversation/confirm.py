import messages
from data_structure.data_structure import DataSet
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from .metadata_action import FilterMetadataAction, MetadataAction
from .binary_action import BinaryAction
from geco_conversation import *
from .empty_state import EmptyAction


class Confirm(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):

        if message is None:
            print(self.status)
            self.context.add_bot_msgs([Utils.chat_message("You can see your choices in the bottom right panel.\nDo you want to keep your selection?"), Utils.param_list(self.status['fields'])])
            return None, False

        if self.context.payload.back!= MetadataAction:
            if intent == "affirm":
                self.context.add_bot_msgs([Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)])
                return RenameAction(self.context), False
            else:
                self.context.add_bot_msgs([Utils.chat_message("Do you want to restart the selection from scratch?")])
                return ChangeSelectionAction(self.context), False

        else:
            if intent == "affirm":
                fields = self.status['fields'].copy()
                del(fields['metadata'])
                del(fields['name'])
                urls = self.context.payload.database.download_filter_meta(fields,self.status['fields']['metadata'])

                self.context.add_bot_msgs([Utils.chat_message("You can download the data by clicking on the arrow in the bottom panel."),Utils.chat_message(messages.other_dataset), Utils.workflow('Data selection', True, urls)])
                return StartAction(self.context), False

class RenameAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )

        urls = self.context.payload.database.download(self.status['fields'])

        ds = DataSet(self.status['fields'], name)
        self.context.data_extraction.datasets.append(ds)
        self.status['fields'].update({'name':name})
        fields = {x: self.status['fields'][x] for x in self.status['fields'] if x in self.status['fields']}

        self.context.add_bot_msgs([Utils.chat_message("OK, dataset saved with name: " + name + ".\nYou can download the data by clicking on the arrow in the bottom panel."),
                Utils.param_list(fields), Utils.workflow('Data selection', True, urls)])
        return FilterMetadataAction(self.context), True


class ChangeSelectionAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['geno_surf', 'dataset_list']

    def logic(self, message, intent, entities):
        if intent == "affirm":
            from .start_action import StartAction
            return StartAction({}), True
        else:
            list_param = {x: x for x in self.status['fields']}
            self.logic = self.change_single_field_logic
            self.context.add_bot_msgs([Utils.chat_message("Which field do you want to change?"),
                    Utils.choice("Fields selected", list_param)])
            return ChangeFieldAction(self.context), False

class ChangeFieldAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['geno_surf', 'dataset_list']


    def logic(self, message, intent, entities):
        selected_field = message.strip().lower()

        if selected_field in self.status['fields']:
            list_param = {x: x for x in getattr(self.context.payload.database, str(selected_field) + '_db')}
            fields = {k:v for (k,v) in self.status['fields'].items() if k != selected_field}
            self.context.add_bot_msgs([Utils.choice(str(selected_field), list_param)])
            return self.status['back'](self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message("The field is not valid, please select another one")])
            return None, False

