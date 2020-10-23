from .pivot_action import PivotAction
from geco_conversation import *

class UnionAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        self.context.data_extraction
        names = {}
        for i in range(len(self.status['dataset_list'])):
            names["DS_" + str(i)] = self.status['dataset_list'][i].name

        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.status['dataset_list']) +1 )
        names['Union']=name

        return [Utils.chat_message("OK, dataset saved with name: " + name),
                Utils.chat_message(messages.other_dataset), Utils.param_list(names),
                ],\
               None, {}
    #
    # def next_action_logic(self, message, intent, entities):
    #     if intent == "affirm":
    #         msgs = []
    #         next_state = StartAction({})
    #     elif intent == "retrieve_annotations":
    #         msgs = []
    #         next_state = AnnotationAction(entities)
    #     elif intent == "retrieve_experiments":
    #         msgs = []
    #         next_state = ExperimentAction(entities)
    #     else:
    #         msgs = [Utils.workflow('Table creation')]
    #         next_state = PivotAction({})
    #
    #     return msgs, next_state, {}