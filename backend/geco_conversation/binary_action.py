from messages import messages
from utils.utils import Utils
from .abstract_action import AbstractAction
from .union_action import UnionAction
from .join_action import JoinAction

class BinaryAction(AbstractAction):

    def on_enter_messages(self):
        list_param = {"Join":'join', "Union":'union', "Difference":'difference', "Map":'map'}
        print(self.status)
        return [Utils.chat_message(messages.start_binary),
                Utils.choice("Binary operations", list_param)], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.binary_help)]

    def required_additional_status(self):
        return []

    def logic(self, message, intent, entities):
        if intent == 'join':
            msg = []
            next_node = JoinAction({})
            new_status= {}
        elif intent == 'union':
            msg = []
            next_node = UnionAction({})
            new_status= {}
        elif intent == 'difference':
            msg = [Utils.chat_message('Sorry, this option is not implemented yet.')]
            next_node = None
            new_status= {}
        else:
            msg = [Utils.chat_message("Sorry, I did not get. Which operation do you want to perform?")]
            next_node = None
            new_status = {}
        return msg, next_node, new_status
