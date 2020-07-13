import messages
import random
import jokes
from .utils import Utils
from .abstract_action import AbstractAction
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from get_api import Geno_surf, experiment_fields, annotation_fields

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
        if intent == 'retrieve_annotations':
            msg = [Utils.workflow('Data selection')]
            next_node = AnnotationAction(entities)
            new_status= {'geno_surf': Geno_surf(annotation_fields, True)}
        elif intent == 'retrieve_experiments':
            msg = [Utils.workflow('Data selection')]
            next_node = ExperimentAction(entities)
            new_status= {'geno_surf': Geno_surf(experiment_fields, False)}
        elif intent == 'name':
            msg = [Utils.chat_message(messages.gecoagent)]
            next_node = None
            new_status = {}
        elif intent == 'mood':
            msg = [Utils.chat_message(messages.mood)]
            next_node = None
            new_status = {}
        elif intent == 'joke':
            joke = random.choice(jokes.jokes)
            msg = [Utils.chat_message(joke)]
            next_node = None
            new_status = {}
        else:
            msg = [Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')]
            next_node = None
            new_status = {}
        return msg, next_node, new_status
