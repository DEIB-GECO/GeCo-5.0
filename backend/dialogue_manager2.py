import copy
from abc import ABC, abstractmethod
from geco_utilities.utils import Utils
from geco_utilities import messages
from workflow.gmql import Select
from data_structure.context import Context
from data_structure.database import DB, annotation_fields, experiment_fields, fields
from data_structure.dataset import DataSet


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

    @abstractmethod
    def to_fill(self):
        pass

    @abstractmethod
    def fill(self, message=None):
        pass

    def run(self, message, intent, entities):
        if intent == "help":
            self.help_message()
            return None, False
        else:
            return self.logic(message, intent, entities)

class StartAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))
        return None, False

    def to_fill(self):
        pass

    def fill(self, message=None):
        pass

    def logic(self, message, intent, entities):
        from knowledge_base import kb
        bool = True
        if intent in kb:
            self.context.frame = kb[intent]
            if intent == 'retrieve_annotations':
                self.context.payload.database = DB(annotation_fields, True, copy.deepcopy(self.context.payload.original_db))
                #self.context.frame={i:{'user':None, 'bot':None, 'message':'Please provide a {}'.format(i)} for i in annotation_fields}
                #for i in annotation_fields:
                #    if i in self.status:
                #        self.context.modify_frame(i, self.status[i])
                #self.context.frame.add(Select(DataSet({'is_annotation':True})))

            elif intent == 'retrieve_experiments':
                self.context.add_bot_msg(Utils.workflow('Data selection'))
                self.context.payload.database = DB(experiment_fields, False,
                                                   copy.deepcopy(self.context.payload.original_db))  # copy.deepcopy(exp_db)
                #self.context.frame.add(Select(DataSet({'is_annotation':False})))
            else:
                self.context.payload.database = DB(fields, None,
                                                   copy.deepcopy(self.context.payload.original_db))
            next_node = self.context.frame[0](self.context)
        else:
            self.context.add_bot_msgs([Utils.chat_message("Sorry, I did not get. Do you want to select annotations or experiments?"),Utils.workflow('Data selection')])
            next_node = None
            bool = False
        return next_node, bool

class CheckDataset(AbstractAction):
    def __init__(self, context):
        super().__init__(context)
        gcm_filter = {k: v for (k, v) in self.status.items() if
                      k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values}
        self.context.payload.database.update(gcm_filter)
        if len(set(self.context.payload.database.table['dataset_name']))==1:
            self.ds_name = set(self.context.payload.database.table['dataset_name'].values)

    def help_message(self):
        return [Utils.chat_message(messages.start_help)]

    def to_fill(self):
        return 'ds_name'

    def fill(self, message):
        if 'dataset_name' in self.status:
            if len(self.status['dataset_name'])==1:
                self.ds_name = self.status['dataset_name']
        else:
            names = message.split(';')
            self.context.modify_status({'dataset_name': names})
            if len(names)==1:
                self.ds_name = self.status['dataset_name']

    def on_enter(self):
        self.context.add_bot_msg(Utils.workflow('Data selection'))
        if hasattr(self, self.to_fill()):
            self.context.add_bot_msg(Utils.chat_message("Ok, you can download your dataset {}".format(self.ds_name)))
            for i in range(len(self.context.frame)):
                if isinstance(self.context.frame[i],type(self)):
                    next_node = self.context.frame[i+1]
                    return next_node(self.context), True
        else:
            ds_names = self.context.payload.database.table['dataset_name'].values
            ds_names = {i: i for i in ds_names}
            self.context.add_bot_msgs([Utils.chat_message("Do you want only one among these? Insert the name, if more separate them with a ';'"),Utils.choice("Available datasets", ds_names)])
        return None, False

    def logic(self, message, intent, entities):
        print('we')
        self.fill(message)
        gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values}
        self.context.payload.database.update(gcm_filter)
        if len(self.status['dataset_name']) == 1:
            self.context.add_bot_msg(Utils.chat_message("Ok, you can download your dataset {}".format(self.ds_name)))

            for i in range(len(self.context.frame)):
                #if isinstance(self.context.frame[i],type(self)):
                if self.context.frame[i].__name__ == type(self).__name__:
                    next_node = self.context.frame[i+1]
                    return next_node(self.context), True
        else:
            self.context.add_bot_msgs(
                [Utils.chat_message("How do you want to put them togheter?")])
        return None, False


class Pivot(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.start_help)]


    def to_fill(self):
        return ['region_column','region_value','metadata_row']

    def fill(self, message=None):
        if 'region_column' in self.status:
            self.region_column = self.status['region_column']
        if 'region_value' in self.status:
            self.region_value = self.status['region_value']
        if 'metadata_row' in self.status:
            self.region_value = self.status['metadata_row']

    def on_enter(self):
        self.fill()
        to_fill = self.to_fill()
        bool = False
        for i in to_fill:
            if hasattr(self, i):
                bool = True
            elif not hasattr(self, i) and not bool:
                self.context.add_bot_msg(Utils.chat_message(messages.pivot_message))
                self.context.add_bot_msg(Utils.chat_message(
                    'You have to define what to put in the table. Which {} do you want?'.format(i)))
                return None, False
            elif not hasattr(self, i):
                self.context.add_bot_msg(Utils.chat_message('Which {} do you want?'.format(i)))
                return None, False

        for i in range(len(self.context.frame)):
            if isinstance(self.context.frame[i], type(self)):
                next_node = self.context.frame[i + 1]
                return next_node, True


    def logic(self, message, intent, entities):
        self.fill()
        to_fill = self.to_fill()
        for i in to_fill:
            if not hasattr(self, i):
                self.context.add_bot_msg(Utils.chat_message('Which {} do you want?'.format(i)))
                return None, False

        self.context.workflow.add(
                Pivot(self.context.workflow[-1], region_column=self.region_column,
                      metadata_row=self.metadata_row, region_value=self.region_value))
        #self.context.workflow.run(self.context.workflow[-1])
        self.context.add_bot_msgs([Utils.chat_message('Pivot is complete. Let\'s proceed')])

        for i in range(len(self.context.frame)):
            if isinstance(self.context.frame[i], type(self)):
                next_node = self.context.frame[i + 1]
                return next_node, True


class Classification(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.start_help)]


    def to_fill(self):
        return ['classifier','tuning']

    def fill(self, message=None):
        if 'classifier' in self.status:
            self.classifier = self.status['classifier']
        if 'tuning' in self.status:
            self.tuning = self.status['tuning']

    def on_enter(self):
        self.fill()
        to_fill = self.to_fill()
        for i in to_fill:
            if not hasattr(self, i) and i=='classifier':
                self.context.add_bot_msg(Utils.chat_message('Which {} do you want?'.format(i)))
                return None, False
            elif not hasattr(self, i) and i=='tuning':
                self.context.add_bot_msg(Utils.chat_message('My advise is to do parameter tuning. Do you want it?'))
                return None, False

        next_node = self.classifier()(self.context)
        return next_node, True


    def logic(self, message, intent, entities):
        self.fill()
        to_fill = self.to_fill()
        for i in to_fill:
            if not hasattr(self, i) and i == 'classifier':
                self.context.add_bot_msg(Utils.chat_message('Which {} do you want?'.format(i)))
                return None, False
            elif not hasattr(self, i) and i == 'tuning':
                self.context.add_bot_msg(Utils.chat_message('My advise is to do parameter tuning. Do you want it?'))
                return None, False

        next_node = self.classifier()(self.context)
        return next_node, True