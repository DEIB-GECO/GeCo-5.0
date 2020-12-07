from data_structure.context import Context
from geco_utilities.utils import Utils
from geco_utilities import messages
from data_structure.database import DB, fields
from data_structure.aggregates import Aggregate
import copy
from data_structure.frame import PivotIndexes
from data_structure.dataset import DataSet


class DM:
    def __init__(self):
        from app import all_db
        self.context = Context(all_db)
        self.frame = self.context.frame
        self.context.payload.database = DB(fields, None,
                                           copy.deepcopy(self.context.payload.original_db))
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
            gcm_filter = {}
            for k, v in self.context.payload.status.items():
                if k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values:
                    gcm_filter[k] = v
                elif len(v) > 1 and v not in self.context.payload.database.table[k].values:
                    val = [i for i in v if i in self.context.payload.database.table[k].values]
                    gcm_filter[k] = val
            self.frame.update_frame(entities, gcm_filter)
            self.run(message, intent)

    def receive(self, message, intent, entities):
        if intent == 'back':
            self.context.pop()
        else:
            self.context.add_user_msg(message)
            self.context.modify_status(entities)
            gcm_filter = {}
            for k, v in self.context.payload.status.items():
                if k in self.context.payload.database.fields and v in self.context.payload.database.table[k].values:
                    gcm_filter[k] = v
                elif len(v) > 1 and v not in self.context.payload.database.table[k].values:
                    val = [i for i in v if i in self.context.payload.database.table[k].values]
                    gcm_filter[k] = val
            self.frame.update_frame(entities, gcm_filter)
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
            workflow = self.frame.create_workflow()
            self.context.add_bot_msgs([Utils.chat_message('Here there is your table of the data selected and you can download the workflow.'), Utils.param_list(attributes),
                                       Utils.workflow(str(type(workflow[-1]).__name__), download=True, link_list=workflow.visualize())])


class CheckDataset():
    def __init__(self, context):
        self.context = context

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
            ds_name = list(set(self.context.payload.database.table['dataset_name'].values))[0]
            gcm_filter.update({'dataset_name': ds_name})
            regions = self.context.payload.database.retrieve_region(ds_name)
            self.context.frame.datasets.append(DataSet(gcm_filter, gcm_filter['dataset_name'], meta_schema=self.context.payload.database.meta_schema, region_schema=regions.columns.values))


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
            ds_name = list(set(self.context.payload.database.table['dataset_name'].values))[0]
            if 'dataset_name' not in gcm_filter:
                gcm_filter.update({'dataset_name':ds_name})
                regions = self.context.payload.database.retrieve_region(ds_name)
                self.context.frame.datasets.append(DataSet(gcm_filter, gcm_filter['dataset_name'],
                                               meta_schema=self.context.payload.database.meta_schema,
                                               region_schema=regions.columns.values))

            self.context.add_step(action=self)
            self.context.add_bot_msgs([
                Utils.chat_message("Ok, I select this dataset {}. Is it correct?".format(ds_name)),Utils.workflow('Data Selection')])
            return False
        else:
            ds = set(self.context.payload.database.table['dataset_name'])

            self.context.add_step(action=self)
            if len(set(self.context.payload.database.table['assembly']))==2:
                self.context.add_bot_msgs(
                    [Utils.chat_message("Which dataset do you want? You can choose only the ones with the same assembly, if you want more"),
                     Utils.choice('Available Datasets', {str(i.split('_')): i for i in ds}),Utils.workflow('Data Selection')])
            else:
                self.context.add_bot_msgs(
                    [Utils.chat_message("Which dataset do you want?"), Utils.choice('Available Datasets',{str(i.split('_')):i for i in ds}),Utils.workflow('Data Selection')])

            return True

class AskRowCol:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        self.context.add_bot_msgs([Utils.chat_message("Do you want features or samples in the rows?"),Utils.workflow('Pivot')])
        return True

    def receive(self, message, intent):
        if message in ['features','feature']:
            self.context.frame.row = PivotIndexes.FEATURES
            self.context.frame.column = PivotIndexes.SAMPLES
        else:
            self.context.frame.row = PivotIndexes.SAMPLES
            self.context.frame.column = PivotIndexes.FEATURES

class AskRegionValue:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        regions = {i:i for i in self.context.payload.database.region_table.columns.values if i not in ['gene_symbol', 'mirna_id', 'entrez_gene_id', 'ensembl_id']}
        self.context.add_bot_msgs([Utils.chat_message("Which value do you want to see in the table?"),
                                   Utils.choice('Available regions', regions)])
        return True

    def receive(self, message, intent):
        self.context.frame.region_value = message

class AskTuning:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        self.context.add_bot_msgs([Utils.chat_message("It is advised to make me apply the parameter tuning. Do you want it?"),Utils.workflow('Clustering')])
        return True

    def receive(self, message, intent):
        if intent=='affirm':
            self.context.frame.tuning = True
        else:
            self.context.frame.tuning = False
            self.context.frame.parameters = None

class AskParametersClustering:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step(action=self)
        self.context.add_bot_msgs([Utils.chat_message("How many clusters do you want?")])
        return True

    def receive(self, message, intent):
        del(self.context.frame.parameters)
        self.context.frame.num_clusters = message


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
            self.context.frame.gmql_binary_operation = UnionAction
        elif message == 'join':
            self.context.frame.gmql_binary_operation = JoinAction
        elif message == 'map':
            self.context.frame.gmql_binary_operation = MapAction
        elif message == 'joinPivot':
            self.context.frame.pivot_binary_operation = JoinPivotAction
        elif message == 'concatPivot':
            self.context.frame.pivot_binary_operation = ConcatPivotAction
        #else:
         #   self.context.add_bot_msgs(
         #       [Utils.chat_message("Sorry, I did not understand")])
        return False

class ConcatPivotAction:
    pass

class JoinPivotAction:
    pass

class UnionAction:
    pass

class JoinAction:
    def __init__(self, context):
        self.context = context
        self.joinby = None

    def run(self):
        self.context.add_step(action=self)
        meta = {i: i for i in self.context.payload.database.meta_schema}
        self.context.add_bot_msgs([Utils.chat_message("Do you want to add a metadatum for the joinby?\nIf so, which one?"),
                                   Utils.choice("Available metadatum", meta)])
        return True

    def receive(self, message, intent):
        if intent!='deny':
            self.joinby = message
        return False

class MapAction:
    def __init__(self, context):
        self.context = context
        self.pos = None
        self.joinby = None
        self.aggregate = None
        self.name_agg = None

    def run(self):
        self.context.add_step(action=self)
        meta = {i:i for i in self.context.payload.database.meta_schema}
        self.context.add_bot_msgs(
            [Utils.chat_message("Do you want to add a metadatum for the joinby?\nIf so, which one?"),
             Utils.choice("Available metadatum", meta)])
        return True

    def receive(self, message, intent):
        if self.joinby==None and self.pos==None:
            self.pos = 'joinby'
            if intent != 'deny':
                self.joinby = message
                agg = {i:i for i in Aggregate.values}
                self.context.add_step(action=self)
                self.context.add_bot_msgs(
                    [Utils.chat_message("Is it ok to count the region?\nIf you want another function, which one?"),
                     Utils.choice("Available functions", agg)])
            return True
        elif self.aggregate==None and self.pos=='joinby':
            self.pos = 'aggregate'
            if intent != 'affirm':
                self.aggregate = Aggregate.switch(message)
                self.context.add_step(action=self)
                self.context.add_bot_msgs(
                    [Utils.chat_message("Do you want to rename the new aggregate?")])
            return True
        elif self.name_agg==None and self.pos=='aggregate':
            self.pos = 'name_agg'
            if intent != 'deny':
                self.name_agg = message

        return False