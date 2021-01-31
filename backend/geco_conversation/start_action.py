from geco_conversation import *
from .abstract_action import AbstractAction
from data_structure.database import DB, fields, experiment_fields, annotation_fields#, ExperimentDB, AnnotationDB#, exp_db, ann_db
import copy

class StartAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def check_status(self):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in self.context.payload.database.fields:
                self.context.payload.replace(k, [x for x in v if
                                                 x in self.context.payload.database.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

    def filter(self, gcm_filter):
        if len(gcm_filter) > 0:
            self.context.payload.database.update(gcm_filter)
        samples = self.context.payload.database.check_existance(gcm_filter)
        return samples

    def on_enter(self):
        self.context.payload.database = DB(fields, True, copy.deepcopy(self.context.payload.original_db))
        list_param = {'Annotations': 'annotations', 'Experimental data': 'experiments'}
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))
        self.context.add_bot_msg(Utils.choice("Data available", list_param))
        self.context.add_bot_msg(Utils.workflow('Data selection'))
        return None, False

    def logic(self, message, intent, entities):
        bool = True
        if intent == 'retrieve_annotations':
            self.context.add_bot_msg(Utils.chat_message('Am I understanding correct the intent and the entities?'))
            self.check_status()
            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
            samples = self.filter(gcm_filter)
            self.context.payload.insert('intent','retrieve_annotation')

            self.context.add_bot_msg(
                Utils.param_list({k: v for (k, v) in self.status.items()}))
            self.context.payload.insert('initial_msg', message)
            next_node = AnnotationAction(self.context)
        elif intent == 'retrieve_experiments':
            next_node = ExperimentAction(self.context)
            self.context.add_bot_msg(Utils.chat_message('Am I understanding correct the intent and the entities?'))
            self.context.payload.insert('intent', 'retrieve_experiment')
            self.check_status()
            gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
            samples = self.filter(gcm_filter)
            self.context.add_bot_msg(Utils.param_list({k: v for (k, v) in self.status.items()}))
            self.context.payload.insert('initial_msg', message)
        else:
            self.context.add_bot_msg([Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')])
            next_node = None
            bool = False
        return UnderstandAction(self.context), False

class UnderstandAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent=='affirm':
            self.context.add_bot_msg([Utils.chat_message('Ok thank you! Bye')])
            return None, False
        else:
            self.context.add_bot_msg(Utils.chat_message('Please tell me is the intent correct?'))
            return IntentAction(self.context), False
        return None, False

class IntentAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent=='affirm':
            self.context.add_bot_msg(Utils.chat_message('Tell me the name of the entities(among the ones on the right) and the value you want separated with :. '
                                                        'If more are wrong, separate them with ;. E.g. disease: kidney renal clear cell carcinoma, kirc; data_type: gene expression quantification, gene expressions'
                                                        'Instead, if you want only to remove some of them tell me "remove"'))
            return EntitiesAction(self.context),False
        elif intent=='deny':
            self.context.add_bot_msg(Utils.chat_message('Which intent are you referring to?'))
            intents = []
            with open('./rasa_files/nlu.md', 'r') as f:
                for line in f:
                    if line.startswith('## intent:'):
                        string = line[10:-1]
                        intents.append(string)
            f.close()
            self.context.add_bot_msg(Utils.choice('Intents',{i: i for i in intents}))
            return None, False

        else:
            self.context.payload.replace('intent', message)

            self.context.add_bot_msg(Utils.chat_message('Please, tell me in this format the name of the entities(among the ones on the right): the value you want, the piece of message that corresponds to it.'
                                                        'If more are wrong, separate them with ;. E.g. disease: kidney renal clear cell carcinoma, kirc; data_type: gene expression quantification, gene expressions'
                                                        'Instead, if you want to remove some of them tell me "remove"'))
            return EntitiesAction(self.context),False



class EntitiesAction(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if message.split()!=['remove'] and intent!='affirm':
            msg = message.split(';')
            for i in msg:
                entity = i.split(':')
                print(entity)
                value = entity[-1].split(',')
                if entity[0] in self.status:
                    self.context.payload.replace(entity[0],value[0])
                else:
                    self.context.payload.insert(entity[0], value[0])
                if 'entities_in_msg' in self.status:
                    self.context.payload.update('entities_in_msg', {entity[0]:{value[0]:value[-1]}})
                else:
                    self.context.payload.insert('entities_in_msg', {entity[0]: {value[0]: value[-1]}})
            self.context.add_bot_msg(Utils.chat_message('Ok, do you want to remove some that are wrong?'))
            self.context.add_bot_msg(Utils.param_list({k: v for (k, v) in self.status.items()}))
            return None, False
        elif message.split()==['remove'] or intent=='affirm':
            self.context.add_bot_msg(Utils.chat_message('Tell me which one you want to remove, separated with ;'))
            return Entities2Action(self.context), False
        elif intent!='deny':
            return Entities2Action(self.context), True

class Entities2Action(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        if self.status['intent'] == 'retrieve_annotation':
            return AnnotationAction(self.context), True
        elif self.status['intent'] == 'retrieve_experiment':
            return ExperimentAction(self.context), True

    def logic(self, message, intent, entities):
        list_remove = message.split(';')
        for i in list_remove:
            if i in self.status:
                self.context.payload.delete(i, self.status[i])
        self.context.add_bot_msg(Utils.param_list({k:self.status[k] for k in self.status}))
        with open('./rasa_files/nlu.md', 'w+') as f:
            msg = self.status['initial_msg']
            for line in f:
                if line.startswith('## intent: ' + self.status['intent']):
                    break
            f.write('- ' + self.status['initial_msg'][0])
        f.close()
        if self.status['intent'] == 'retrieve_annotation':
            return AnnotationAction(self.context), True
        elif self.status['intent'] == 'retrieve_experiment':
            return ExperimentAction(self.context), True
