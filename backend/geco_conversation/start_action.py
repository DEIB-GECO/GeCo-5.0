from geco_conversation import *
from .abstract_action import AbstractAction
from data_structure.database import DB, experiment_fields, annotation_fields#, ExperimentDB, AnnotationDB#, exp_db, ann_db
import copy

class StartAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        list_param = {'Annotations': 'annotations', 'Experimental data': 'experiments'}
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))
        self.context.add_bot_msg(Utils.choice("Data available", list_param))
        self.context.add_bot_msg(Utils.workflow('Data selection'))
        return None, False

    def logic(self, message, intent, entities):
        bool = True
        if intent == 'retrieve_annotations':
            self.context.payload.database = DB(annotation_fields, True, copy.deepcopy(self.context.payload.original_db))
            next_node = AnnotationAction(self.context)
        elif intent == 'retrieve_experiments':
            next_node = ExperimentAction(self.context)
            self.context.payload.database = DB(experiment_fields, False, copy.deepcopy(self.context.payload.original_db))#copy.deepcopy(exp_db)
        else:
            self.context.add_bot_msgs([Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')])
            next_node = None
            bool = False
        return next_node, bool
