from geco_conversation import *
from .abstract_action import AbstractAction
from data_structure.database import DB, experiment_fields, annotation_fields#, ExperimentDB, AnnotationDB#, exp_db, ann_db
import copy

class StartAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.start_help)])
        return None, True

    def on_enter(self):
        list_param = {'Annotations': 'annotations', 'Experimental data': 'experiments'}
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))
        self.context.add_bot_msg(Utils.choice("Data available", list_param))
        #self.context.add_bot_msg(Utils.scatter([1,2,3], [1,2,3], [0, 3, 2], {0, 3, 2}))
        self.context.add_bot_msg(Utils.workflow('Data selection'))
        return StartAction(self.context), False

    def logic(self, message, intent, entities):
        bool = True
        if intent == 'retrieve_annotations':
            self.context.payload.database = DB(annotation_fields, True, copy.deepcopy(self.context.payload.original_db))
            next_node = AnnotationAction(self.context)
        elif intent == 'retrieve_experiments':
            self.context.payload.database = DB(experiment_fields, False, copy.deepcopy(self.context.payload.original_db))
            next_node = ExperimentAction(self.context)
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.wrong_exp_ann),
                                       Utils.workflow('Data selection')])
            next_node = StartAction(self.context)
            bool = False
        return next_node, bool
