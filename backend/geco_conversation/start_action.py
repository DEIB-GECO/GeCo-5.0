import messages
from .utils import Utils
from .abstract_action import AbstractAction
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from database import DB, experiment_fields, annotation_fields

class StartAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def required_additional_status(self):
        return []

    def logic(self, message, intent, entities):
        if message is None:
            list_param = {'Annotations': 'annotations', 'Experimental data': 'experiments'}
            self.context.add_bot_msg(Utils.chat_message(messages.start_init))
            self.context.add_bot_msg(Utils.choice("Data available", list_param))
            self.context.add_bot_msg(Utils.workflow('Data selection'))
            return None, False
        elif intent == 'retrieve_annotations':
            self.context.add_bot_msg(Utils.workflow('Data selection'))
            next_node = AnnotationAction(self.context)
            self.context.payload.database = DB(annotation_fields, True)
        elif intent == 'retrieve_experiments':
            self.context.add_bot_msg(Utils.workflow('Data selection'))
            next_node = ExperimentAction(self.context)
            self.context.payload.database = DB(experiment_fields, False)
        else:
            self.context.add_bot_msg([Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')])
            next_node = None
        return  next_node, True
