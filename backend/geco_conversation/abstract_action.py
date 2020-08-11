from abc import ABC, abstractmethod
from geco_conversation.utils import Utils
import messages
import random
import requests
import jokes
import json
import copy


class AbstractAction(ABC):
    def __init__(self, status):
        self.status = status
        self.backup_status = None

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
        elif intent == "back":
            self.restore_backup()
            print('logic1')
            if self.backup_status.entities!=None and self.backup_status.intent!=None:
                print('logic')
                print(self.logic)
                return self.logic(message, self.backup_status.intent, self.backup_status.entities)
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
        elif intent == 'weather':
            response = requests.get('https://www.metaweather.com/api/location/718345/')
            msg = [Utils.chat_message('Here in Milan the weather forecast says: ' + json.loads(response.content.decode('utf-8'))['consolidated_weather'][0]['weather_state_name'].lower())]
            return msg, None, {}
        else:
            return self.logic(message, intent, entities)

    def create_backup(self, intent=None, entities=None):
        self.backup_status = BackupStatus(self.logic, copy.deepcopy(self.status), intent, entities)


    def restore_backup(self):
        print('BACKUP')
        print(self.backup_status.logic)
        print(self.backup_status.status)
        if self.backup_status!=None:
            self.logic = self.backup_status.logic
            self.status = copy.deepcopy(self.backup_status.status)



class BackupStatus:
    def __init__(self, logic, status, intent = None,  entities = None):
        self.logic = logic
        self.status = status
        self.entities = entities
        self.intent = intent
        #self.message = message


