import messages
from .utils import Utils
from .abstract_action import AbstractAction
from .start_action import StartAction

class EmptyAction(AbstractAction):

    def on_enter_messages(self):
        return [], None, {}

    def help_message(self):
        return []

    def required_additional_status(self):
        return []

    def logic(self, message, intent, entities):

        return [], StartAction({}), {}
