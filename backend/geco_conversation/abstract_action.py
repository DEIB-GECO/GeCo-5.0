from abc import ABC, abstractmethod
from geco_conversation import *
import random
import requests
import json


class AbstractAction(ABC):
    def __init__(self, context):
        self.context = context
        self.status = self.context.payload.status

    @abstractmethod
    def help_message(self):
        pass

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def logic(self, message, intent, entities):
        pass

    def run(self, message, intent, entities):
        if intent == "help":
            self.help_message()
            #return None, False
        else:
            return self.logic(message, intent, entities)
        '''
        elif intent == 'name':
            self.context.add_bot_msgs([Utils.chat_message(messages.gecoagent)])
            return None, False
        elif intent == 'mood':
            self.context.add_bot_msgs([Utils.chat_message(messages.mood)])
            return None, False
        elif intent == 'joke':
            joke = random.choice(jokes.jokes)
            self.context.add_bot_msgs([Utils.chat_message(joke)])
            return None, False
        elif intent == 'weather':
            response = requests.get('https://www.metaweather.com/api/location/718345/')
            self.context.add_bot_msgs([Utils.chat_message('Here in Milan the weather forecast says: ' + json.loads(response.content.decode('utf-8'))['consolidated_weather'][0]['weather_state_name'].lower())])
            return None, False
       '''
        #else:
         #   return self.logic(message, intent, entities)


class AbstractDBAction(AbstractAction):
    def __init__(self, context):
        self.context = context
        self.status = self.context.payload.status
        self.db = self.context.payload.database
        self.db_table = self.db.table

    @abstractmethod
    def help_message(self):
        pass

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def logic(self, message, intent, entities):
        pass

    def run(self, message, intent, entities):
        if intent == "help":
            self.help_message()
            #return None, False
        else:
            return self.logic(message, intent, entities)


