from abc import ABC, abstractmethod
from geco_conversation.utils import Utils
import messages
import random
import jokes


class AbstractAction(ABC):
    def __init__(self, status):
        self.status = status

    @abstractmethod
    def on_enter_messages(self):
        pass

    @abstractmethod
    def required_additional_status(self):
        pass

    @abstractmethod
    def help_message(self):
        pass


    @abstractmethod
    def logic(self, message, intent, entities):
        pass

    def add_additional_status(self, additional_status):
        for k in additional_status:
            self.status[k] = additional_status[k]

    def run(self, message, intent, entities):
        if intent == "help":
            return self.help_message(), None, {}
        elif intent == 'name':
            msg = [Utils.chat_message(messages.gecoagent)]
            return msg, None, {}
        elif intent == 'mood':
            msg = [Utils.chat_message(messages.mood)]
            return msg, None, {}
        elif intent == 'joke':
            joke = random.choice(jokes.jokes)
            msg = [Utils.chat_message(joke)]
            return msg, None, {}
        else:
            return self.logic(message, intent, entities)

