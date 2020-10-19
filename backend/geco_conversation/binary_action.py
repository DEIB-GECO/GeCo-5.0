from .abstract_action import AbstractAction
from .union_action import UnionAction
from .join_action import JoinAction
from geco_conversation import *

class BinaryAction(AbstractAction):


    def help_message(self):
        return [Utils.chat_message(messages.binary_help)]


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
