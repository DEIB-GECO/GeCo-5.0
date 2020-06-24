import messages
from .annotation_action import AnnotationAction
from .experiment_action import ExperimentAction
from geco_conversation import *

class PivotAction(AbstractAction):

    def on_enter_messages(self):
        return [Utils.chat_message(messages.pivot_message)], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def required_additional_status(self):
        return ['dataset_list']

    def logic(self, message, intent, entities):
        self.logic = self.metadata_logic
        return [Utils.chat_message("OK, which metadata do you want to keep in the columns?")], None, {}

    def metadata_logic(self, message, intent, entities):
        self.logic = self.region_logic
        return [Utils.chat_message("And which region data do you want to keep in the columns?")], None, {}

    def region_logic(self, message, intent, entities):
        self.logic = self.value_logic
        return [Utils.chat_message("Finally, what are the values that you want to see?")], None, {}

    def value_logic(self, message, intent, entities):
        return [Utils.chat_message("Here is your table. You can also download it."),Utils.chat_message(messages.bye_message)], None, {}