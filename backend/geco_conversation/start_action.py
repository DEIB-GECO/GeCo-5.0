import messages
from .utils import Utils
from .abstract_action import AbstractAction
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from database import DB, experiment_fields, annotation_fields

class StartAction(AbstractAction):

    def on_enter_messages(self):
        list_param = {'Annotations':'annotations', 'Experimental data':'experiments'}
        return [Utils.chat_message(messages.start_init),
                Utils.choice("Data available", list_param)], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def required_additional_status(self):
        return []

    def logic(self, message, intent, entities):
        self.logic = self.logic_intent
        list_param = {'Annotations': 'annotations', 'Experimental data': 'experiments'}
        return [Utils.chat_message(messages.start_init),
                Utils.choice("Data available", list_param)], None, {}

    def logic_intent(self, message, intent, entities):
        if intent == 'retrieve_annotations':
            msg = [Utils.workflow('Data selection')]
            next_node = AnnotationAction(self.context)
            new_status= {'geno_surf': DB(annotation_fields, True)}
        elif intent == 'retrieve_experiments':
            msg = [Utils.workflow('Data selection')]
            next_node = ExperimentAction(self.context)
            new_status= {'geno_surf': DB(experiment_fields, False)}
        else:
            msg = [Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')]
            next_node = None
            new_status = {}
        return msg, next_node, new_status
