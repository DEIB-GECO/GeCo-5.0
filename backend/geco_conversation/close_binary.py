from messages import messages
from data_structure.data_structure import DataSet
from .metadata_action import MetadataAction
from geco_conversation import *


class Confirm(AbstractAction):

    def on_enter_messages(self):
        return [Utils.chat_message("Do you want to confirm your operation?")], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.confirm_help)]

    def required_additional_status(self):
        return ['final_dataset']

    def logic(self, message, intent, entities):
        if intent == "affirm":
            self.logic = self.set_name_logic
            return [Utils.chat_message("OK"), Utils.chat_message(messages.assign_name)], None, {}
        else:
            self.logic = self.change_binary_logic
            return [Utils.chat_message("Do you want to go back to the selection?")], None, {}

    def set_name_logic(self, message, intent, entities):
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.status['dataset_list']) +1 )


        ds = DataSet(self.status['fields'], name)
        self.status['dataset_list'].append(ds)
        self.status['fields'].update({'name':name})
        self.logic = self.next_action_logic


        return [Utils.chat_message("OK, dataset saved with name: " + name),
                Utils.chat_message(messages.other_dataset)],\
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
        else:
            msgs = []
            fields = {x: self.status['fields'][x] for x in self.status['fields'] if x in self.status['fields']}
            next_state = MetadataAction({'fields': fields})

        return msgs, next_state, {}

    def change_binary_logic(self, message, intent, entities):
        if intent == "affirm":
            return [], AskConfirm({}), {}
        else:
            from .start_action import StartAction
            return [], StartAction({}), {}
