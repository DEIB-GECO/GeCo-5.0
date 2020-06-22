import messages
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from geco_conversation import *

class JoinAction(AbstractAction):

    def on_enter_messages(self):
        return [Utils.chat_message("Do you want to join the two datasets according to patient ID?"), ], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.join_help)]

    def required_additional_status(self):
        return ['dataset_list']

    def logic(self, message, intent, entities):
        self.logic = self.set_name_logic
        if intent != "deny":
            msg =  [Utils.chat_message(messages.assign_name)]
        else:
            msg = [Utils.chat_message('Ok, I will do the cartesian product of all the samples.'),Utils.chat_message(messages.assign_name)]


        return msg, None, {}

    def set_name_logic(self, message, intent, entities):
        self.logic = self.next_action_logic
        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.status['dataset_list']) +1 )


        return [Utils.chat_message("OK, dataset saved with name: " + name),
                Utils.chat_message(messages.other_dataset)
                ],\
               None, {}

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
            # next_state = MetadataAction({'fields': fields})
            next_state = {}

        return msgs, next_state, {}