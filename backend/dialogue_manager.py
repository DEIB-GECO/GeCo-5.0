from data_structure.context import Context
from geco_utilities.utils import Utils
from geco_utilities import messages
from data_structure.database import DB, fields
import copy
from data_structure.frame import PivotIndexes

class DM:
    def __init__(self, interpreter, db):
        self.interpreter = interpreter
        self.context = Context(db)
        self.frame = self.context.frame
        self.context.add_step(bot_msgs=Utils.chat_message(messages.initial_greeting))
        self.enter()

    def enter(self):
        self.context.add_bot_msg(Utils.chat_message(messages.start_init))

    def receive(self, message):
        interpretation = self.interpreter.parse(message)
        intent = interpretation['intent']['name']
        print('intent', intent)

        if intent == 'back':
            self.context.pop()
        else:
            self.context.add_user_msg(message)
            entities = {}
            for e in interpretation['entities']:
                if e['entity'] in entities and e['value'].lower().strip() not in entities[e['entity']]:
                    entities[e['entity']].append(e['value'].lower().strip())
                else:
                    entities[e['entity']] = [e['value'].lower().strip()]
            print('entities', entities)

            self.context.modify_status(entities)
            self.frame.define_frame(intent)
            self.frame.update_frame(entities)
            self.run()


    def run(self):
        filled = self.frame.is_filled()
        if filled!=True:
            for i in filled:
                i(self.context).run()

        else:
            self.context.add_step()
            self.context.add_bot_msg(Utils.chat_message('You filled the frame'))
            print(self.frame.attributes())
            self.context.add_bot_msg(Utils.param_list(self.frame.attributes()))



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
            self.context.frame.datasets.append(ds_name)

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
            self.context.frame.datasets.append(ds_name)
            self.context.add_step()
            self.context.add_bot_msg(
                Utils.chat_message("Ok, you can download your dataset {}".format(ds_name)))
            return
        else:
            self.context.add_step()
            self.context.add_bot_msgs(
                [Utils.chat_message("Which dataset do you want?")])
            #self.run()
            return

class AskRowCol:
    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.add_step()
        self.context.add_bot_msgs([Utils.chat_message("Do you want features or samples in the rows?")])

class ConcatPivot:
    pass

class JoinPivot:
    pass