from geco_conversation import *
from .abstract_action import AbstractAction
from data_structure.database import DB, experiment_fields, annotation_fields#, ExperimentDB, AnnotationDB#, exp_db, ann_db
import copy

class ByeAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msg(Utils.chat_message("You can restart from the beginning or close the page!"))
        return None, True

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message("Do you want to start another analysis from the beginning?"))
        return None, False

    def logic(self, message, intent, entities):
        bool = True
        if intent == 'affirm':
            next_node = StartAction(self.context)
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.bye_message)])
            next_node = None
            bool = False
        return next_node, bool
