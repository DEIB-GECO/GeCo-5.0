from data_structure.context import Context
from geco_utilities.utils import Utils
from geco_utilities import messages
from data_structure.database import DB, fields
import copy
from data_structure.frame import PivotIndexes
from data_structure.dataset import DataSet


class DM:
    def __init__(self):
        from app import all_db
        self.context = Context(all_db)
        self.frame = self.context.frame
        self.context.add_step(bot_msgs=Utils.chat_message(messages.initial_greeting))
        self.enter()

    def enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))

    def receive_first_msg(self, message, intent, entities):

        if intent == 'back':
            self.context.pop()
        else:
            self.context.add_user_msg(message)

            self.context.modify_status(entities)
            self.frame.define_frame(intent)
            self.frame.update_frame(entities)
            self.run(message, intent)

    def receive(self, message, intent, entities):
        if intent == 'back':
            self.context.pop()
        else:
            self.context.add_user_msg(message)

            self.context.modify_status(entities)
            self.frame.update_frame(entities)
            self.run(message, intent)


    def run(self, message, intent):
        filled = self.frame.is_filled()
        if filled!=True:
            for i in filled:
                bool = i(self.context).run()
                if not bool:
                    break
                if hasattr(i,'receive'):
                    i(self.context).receive(message, intent)
                    break

        else:
            self.context.add_step(action=self)
            attributes = self.frame.attributes()
            print(attributes)
            self.context.add_bot_msgs([Utils.chat_message('You filled the frame'), Utils.param_list(attributes)])



class CheckDataset():
    def __init__(self, context):
        self.context = context
        self.context.payload.database = DB(fields, None,
                                           copy.deepcopy(self.context.payload.original_db))
        self.status = self.context.payload.status
        gcm_filter = {}
        for k, v in self.status.items():
            if k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values:
                gcm_filter[k] = v
            elif len(v) > 1 and v not in self.context.payload.database.table[k].values:
                val = [i for i in v if i in self.context.payload.database.table[k].values]
                gcm_filter[k] = val
        self.context.payload.database.update(gcm_filter)
        if len(set(self.context.payload.database.table['dataset_name'])) == 1:
            ds_name = set(self.context.payload.database.table['dataset_name'].values)
            gcm_filter.update({'dataset_name': ds_name})
            self.context.frame.datasets.append(DataSet(gcm_filter, gcm_filter['dataset_name']), meta_schema=self.context.payload.database.meta_schema)


    def run(self):
        gcm_filter={}
        for k,v in self.status.items():
            if k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values:
                gcm_filter[k] = v
            elif len(v)>1 and v not in self.context.payload.database.table[k].values:
                val = [i for i in v if i in self.context.payload.database.table[k].values]
                gcm_filter[k] = val

        self.context.payload.database.update(gcm_filter)
        if len(set(self.context.payload.database.table['dataset_name'])) == 1:
            ds_name = set(self.context.payload.database.table['dataset_name'].values)
            gcm_filter.update({'dataset_name':ds_name})
            self.context.frame.datasets.append(DataSet(gcm_filter, gcm_filter['dataset_name']),
                                               meta_schema=self.context.payload.database.meta_schema)

            self.context.add_step(action=self)
            self.context.add_bot_msg(
                Utils.chat_message("Ok, I select this dataset {}".format(ds_name)))
            return False
        else:
            ds = set(self.context.payload.database.table['dataset_name'])

            self.context.add_step(action=self)
            if len(set(self.context.payload.database.table['assembly']))==2:
                self.context.add_bot_msgs(
                    [Utils.chat_message("Which dataset do you want? You can choose only the ones with the same assembly, if you want more"),
                     Utils.choice('Available Datasets', {str(i.split('_')): i for i in ds})])
            else:
                self.context.add_bot_msgs(
                    [Utils.chat_message("Which dataset do you want?"), Utils.choice('Available Datasets',{str(i.split('_')):i for i in ds})])

            return True

class AskRowCol:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        self.context.add_bot_msgs([Utils.chat_message("Do you want features or samples in the rows?")])
        return True

    def receive(self, message, intent):
        if message in ['features','feature']:
            self.context.frame.row = PivotIndexes.FEATURES
            self.context.frame.column = PivotIndexes.SAMPLES
        else:
            self.context.frame.row = PivotIndexes.SAMPLES
            self.context.frame.column = PivotIndexes.FEATURES

class AskTuning:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        self.context.add_bot_msgs([Utils.chat_message("It is advised to make me apply the parameter tuning. Do you want it?")])
        return True

    def receive(self, message, intent):
        if intent=='affirm':
            self.context.frame.tuning = True
        else:
            self.context.frame.tuning = False

class AskBinary:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        operations = {'Union':'union', 'Join':'join', 'Map':'map', 'Join after the table creation': 'joinPivot', 'Concatenate the two tables': 'concatPivot'}
        self.context.add_bot_msgs([Utils.chat_message("How do you want to put them together? You can decide among different options."),
                                   Utils.choice("Available choices", operations)])
        return True

    def receive(self, message, intent):
        if message=='union':
            self.context.frame.gmql_binary_operation = Union
        elif message == 'join':
            self.context.frame.gmql_binary_operation = Join
        elif message == 'map':
            self.context.frame.gmql_binary_operation = Map
        elif message == 'joinPivot':
            self.context.frame.pivot_binary_operation = JoinPivot
        elif message == 'concatPivot':
            self.context.frame.pivot_binary_operation = ConcatPivot
        #else:
         #   self.context.add_bot_msgs(
         #       [Utils.chat_message("Sorry, I did not understand")])
        return False

class ConcatPivot:
    pass

class JoinPivot:
    pass

class Union:
    pass

class Join:
    pass

class Map:
    pass