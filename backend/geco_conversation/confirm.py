import messages
from data_structure.data_structure import DataSet
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from .metadata_action import MetadataAction
from .binary_action import BinaryAction
from geco_conversation import *


class Confirm(AbstractAction):

    def on_enter_messages(self):
        return [Utils.chat_message("You can see your choices in the bottom right panel.\nDo you want to keep your selection?")], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):
        if intent == "affirm":
            self.logic = self.set_name_logic
            return [Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)], None, {}
        else:
            self.logic = self.change_selection_logic
            return [Utils.chat_message("Do you want to restart the selection from scratch?")], None, {}

    def set_name_logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.status['dataset_list']) +1 )

        urls = self.status['geno_surf'].download(self.status['fields'])

        ds = DataSet(self.status['fields'], name)
        self.status['dataset_list'].append(ds)
        self.status['fields'].update({'name':name})
        self.logic = self.next_action_logic

        print(Utils.workflow('Data selection', True, urls))

        return [Utils.chat_message("OK, dataset saved with name: " + name + ".\nYou can download the data by clicking on the arrow in the bottom panel."),
                Utils.chat_message(messages.other_dataset),
                Utils.param_list(self.status['fields']),
                Utils.workflow('Data selection', True, urls)],\
               None, {"dataset_list": self.status['dataset_list']}

    def next_action_logic(self, message, intent, entities):
        if intent == "affirm":
            msgs = []
            next_state = StartAction({})
        elif intent == "retrieve_annotations":
            msgs = []
            next_state = AnnotationAction(entities)
        elif intent == "retrieve_experiments":
            msgs = []
            next_state = ExperimentAction(entities)
        # elif len(self.status['dataset_list'])==2:
        #    msgs = [Utils.workflow('Dataset elaboration')]
        #    #next_state = MetadataAction({'fields': fields})
        #    next_state = BinaryAction({})
        else:
            msgs = [messages.bye_message, Utils.workflow('END')]
            fields = {x: self.status['fields'][x] for x in self.status['fields'] if x in self.status['fields']}
            #next_state = MetadataAction({'fields': fields})
            next_state = StartAction({})


        return msgs, next_state, {}

    def change_selection_logic(self, message, intent, entities):
        if intent == "affirm":
            from .start_action import StartAction
            return [], StartAction({}), {}
        else:
            list_param = {x: x for x in self.status['fields']}
            self.logic = self.change_single_field_logic
            return [Utils.chat_message("Which field do you want to change?"),
                    Utils.choice("Fields selected", list_param)], None, {}

    def change_single_field_logic(self, message, intent, entities):
        selected_field = message.strip().lower()

        if selected_field in self.status['fields']:
            list_param = {x: x for x in getattr(self.status['geno_surf'], str(selected_field) + '_db')}
            fields = {k:v for (k,v) in self.status['fields'].items() if k != selected_field}
            return [Utils.choice(str(selected_field), list_param)], self.status['back'](fields), {}
        else:
            return [Utils.chat_message("The field is not valid, please select another one")], None, {}

