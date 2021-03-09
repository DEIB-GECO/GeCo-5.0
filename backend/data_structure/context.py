from workflow import Workflow
from ordered_set import OrderedSet

# Class that contains what in a step is changed
class Delta:
    # A new data is saved into the context
    def insert_value(self, name):
        if hasattr(self, 'insertion'):
            self.insertion.append(name)
        else:
            self.insertion = [name]

    # A data in the context is removed
    def delete_value(self, name, value):
        if hasattr(self, 'deletion'):
            self.deletion.append({'variable': name, 'value': value})
        else:
            self.deletion = [{'variable': name, 'value': value}]

    # A data in the context is changed
    def update_value(self, name, old_value, new_value):
        if hasattr(self, 'update'):
            self.update.append({'variable': name, 'new': new_value, 'old': old_value})
        else:
            self.update = [{'variable': name, 'new': new_value, 'old': old_value}]


# Class that define each step of the automa. It contains the action, the bot messages, the received user message and the changed elements in that state
class Step:
    def __init__(self, bot_msgs, action=None, user_msg=None):
        self.action = action
        self.bot_msgs = bot_msgs
        self.user_msg = user_msg
        self.delta = Delta()

    def __repr__(self):
        if self.bot_msgs != None:
            return f'Step:(Action:{self.action}, Bot_msgs:{[i for i in self.bot_msgs if i["type"] == "message" if self.bot_msgs != None]}, User_msg:{self.user_msg})'
        else:
            return f'Step:(Action:{self.action}, Bot_msgs: None, User_msg:{self.user_msg})'

    def __str__(self):
        return self.__repr__()


# Class that define other things in the context. It contain the database and the status.
class Payload:
    def __init__(self, context, db):
        self.context = context
        self.status = {}
        self.original_db = db
        self.database = None

    # Insert something in the status (the action calls the delta function to add the new thing)
    # Insert everything as a list or dictionary
    def insert(self, key, value):
        if isinstance(value, list) or isinstance(value, dict):
            self.status[key] = value
        else:
            self.status[key] = [value]
        self.context.top_delta().insert_value(key)

    # Update something in the status (the action calls the delta function to modify the updated key)
    def update(self, key, new_value):
        old = self.status[key]
        if isinstance(old, list):
            if not isinstance(new_value, list):
                if old != [None]:
                    self.status[key].append(new_value)
                    self.status[key] = list(OrderedSet(self.status[key]))
                else:
                    self.status[key] = [new_value]
            else:
                if old != [None]:
                    self.status[key] = list(OrderedSet(old + new_value))
                else:
                    self.status[key] = list(OrderedSet(new_value))
        elif isinstance(old, dict):
            if isinstance(new_value, dict):
                for k in new_value.keys():
                    if k in old:
                        if isinstance(old[k], list):
                            self.status[key][k].append(new_value[k])
                        else:
                            self.status[key][k] = [self.status[key][k]]
                            self.status[key][k].append(new_value[k])
                    else:
                        self.status[key][k] = new_value[k]
            elif self.status[key]=={}:
                self.status[key] = new_value
            else:
                self.status[key].update(new_value)
        elif old == None:
            if not isinstance(new_value, list):
                self.status[key] = [new_value]
            else:
                self.status[key] = list(set(new_value))
        self.context.top_delta().update_value(key, old, self.status[key])

    # Replace something
    def replace(self, key, new):
        old = self.status[key]
        self.status[key] = new
        if old != new:
            self.context.top_delta().update_value(key, old, self.status[key])

    # Delete a variable in the status
    def delete(self, key, value=None):
        if value == None:
            del (self.status[key])
            self.context.top_delta().delete_value(key, value)
        elif key in self.status and self.status[key] == value:
            del (self.status[key])
            self.context.top_delta().delete_value(key, value)
        elif key in self.status:
            old = self.status[key]
            if isinstance(old, list):
                self.status[key] = old.remove(value)
            elif isinstance(old, dict):
                self.status[key].pop(value)
            # print(self.status[key])
            self.context.top_delta().update_value(key, old, self.status[key])

    def delete_from_dict(self, outer_key, inner_key, value=None):
        if value == None:
            old = self.status[outer_key][inner_key]
            del (self.status[outer_key][inner_key])
            self.context.top_delta().update_value(outer_key, old, self.status[outer_key])
            #self.context.top_delta().delete_value(key, value)
        else:
            old = self.status[outer_key][inner_key]
            if isinstance(old, list):
                if isinstance(value,list):
                    self.status[outer_key][inner_key] = list(set(old)-set(value))
                    if self.status[outer_key][inner_key]==[]:
                        del (self.status[outer_key][inner_key])
                else:
                    self.status[outer_key][inner_key] = old.remove(value)
            elif isinstance(old, dict):
                self.status[outer_key][inner_key].pop(value)
            # print(self.status[key])
            self.context.top_delta().update_value(outer_key, old, self.status[outer_key])

    # Clear the status
    def clear(self):
        for x in self.status:
            self.context.top_delta().delete_value(x, self.status[x])
        self.status.clear()


# Class for saving datasets and operations present in data extraction step (till pivot)
class Data_Extraction:
    def __init__(self):
        self.datasets = []
        self.binary = []
        self.unary = []
        self.table = {}


# Context class that contains:
# - the history composed of steps
# - the payload to save necessary temporary data for the pipeline
# - the workflow, intermediate representation for the operations
class Context:
    def __init__(self, db, session_id):
        self.session_id = session_id
        self.history = []
        self.payload = Payload(self, db)
        self.workflow = Workflow()
        self.data_extraction = Data_Extraction()
        '''
        self.data_analysis = {
            'par_tuning' : [],
            'validation' : [],
            'algorithms' : []
        }
        '''

    # Add a step to the history stack
    def add_step(self, bot_msgs=None, action=None, user_msg=None):
        self.history.append(Step(bot_msgs, action, user_msg))

    # Return all the messages at the top of the history
    def top_bot_msgs(self):
        if self.history[-1].user_msg != None:
            if (self.history[-1].bot_msgs != None):
                return self.history[-1].bot_msgs
            elif (len(self.history) >= 2) and (self.history[-2].bot_msgs != None):
                return self.history[-2].bot_msgs
        else:
            if (self.history[-1].bot_msgs != None):
                if (len(self.history) >= 2) and (self.history[-2].bot_msgs != None):
                    return self.history[-2].bot_msgs + self.history[-1].bot_msgs
                elif (len(self.history) >= 2) and (self.history[-2].bot_msgs == None):
                    return self.history[-1].bot_msgs
            elif (len(self.history) >= 2) and (self.history[-2].bot_msgs != None) and (self.history[-2].user_msg==None):
                if (len(self.history) >= 3) and (self.history[-3].bot_msgs != None):
                    return self.history[-3].bot_msgs + self.history[-2].bot_msgs
                else:
                    return self.history[-2].bot_msgs
            elif (len(self.history) >= 2) and (self.history[-2].bot_msgs != None):
                return self.history[-2].bot_msgs
        return None

    def top_user_msg(self):
        return self.history[-1].user_msg

    def top_action(self):
        return self.history[-1].action

    def top_delta(self):
        return self.history[-1].delta

    def add_user_msg(self, user_msg):
        self.history[-1].user_msg = user_msg

    def add_bot_msg(self, bot_msg):
        if type(self.history[-1].bot_msgs) == list:
            self.history[-1].bot_msgs.append(bot_msg)
        elif self.history[-1].bot_msgs == None:
            self.history[-1].bot_msgs = [bot_msg]
        else:
            self.history[-1].bot_msgs = [self.history[-1].bot_msgs, bot_msg]
        # print(self.history)

    def add_bot_msgs(self, bot_msgs):
        if (self.history[-1].bot_msgs != None):
            if isinstance(self.history[-1].bot_msgs, list):
                self.history[-1].bot_msgs.extend(bot_msgs)
            else:
                self.history[-1].bot_msgs = [self.history[-1].bot_msgs].extend(bot_msgs)
        else:
            self.history[-1].bot_msgs = bot_msgs

    def add_delta(self, delta):
        self.history[-1].delta = delta

    # Remove last step in case of back action
    def pop(self):
        print(self.history)
        if self.history[-1].bot_msgs == None:
            print('before deleted',self.payload.status)
            del (self.history[-1])
            self.revert()
            print('after 1 deleted', self.payload.status)
            action = self.history[-1].action
            del(self.history[-1])
            self.revert()
            if self.history[-1].user_msg == None:
                self.revert()
            self.add_step(action=action)
            bot_msg = self.top_bot_msgs()
            i = -1
            while (bot_msg==None):
                i -=1
                bot_msg = self.history[i].bot_msgs
            if bot_msg!=None:
                self.history[-1].bot_msgs = bot_msg
            print('after 2 deleted', self.payload.status)
        else:
            print('before deleted', self.history[-1])
            del (self.history[-1])
            self.revert()
        #action = self.history[-1].action
        print('dopo', self.history)
        #del (self.history[-1])
        self.add_step(action=action)
        #print('before bot_msg added', self.history[-1])
        i = -1
        #while (self.top_bot_msgs() == None):
         #   i -= 1
        #self.add_bot_msgs(self.history[i].bot_msgs)
        #print('afetr bot_msg added', self.history[-1])
        # self.history[-2].bot_msgs = None

    def last_valid_user_msg(self):
        return self.history[-1].user_msg

    # Remove the saved stuff from the payload in case of back
    def revert(self):
        if hasattr(self.history[-1].delta, 'insertion'):
            for i in self.history[-1].delta.insertion:
                if i in self.payload.status:
                    del (self.payload.status[i])

        if hasattr(self.history[-1].delta, 'deletion'):
            for elem in self.history[-1].delta.deletion:
                self.payload.status[elem['variable']] = elem['value']

        if hasattr(self.history[-1].delta, 'update'):
            for elem in self.history[-1].delta.update:
                self.payload.status[elem['variable']] = elem['old']

        gcm_filter = {k:v for k,v in self.payload.status.items() if k in self.payload.database.fields}
        if gcm_filter!={}:
            self.payload.database.go_back(gcm_filter)

        # if hasattr(self.history[-2].delta, 'insertion'):
        #     for i in self.history[-2].delta.insertion:
        #         del (self.payload.status[i])
        #
        # if hasattr(self.history[-2].delta, 'deletion'):
        #     for elem in self.history[-2].delta.deletion:
        #         self.payload.status[elem['variable']]=elem['value']
        #
        # if hasattr(self.history[-2].delta, 'update'):
        #     for elem in self.history[-2].delta.update:
        #         self.payload.status[elem['variable']]=elem['new_value']

        return

    def modify_status(self, dict):
        for k,v in dict.items():
            if k in self.payload.status:
                self.payload.update(k,list(set(v)))
            else:
                self.payload.insert(k, list(set(v)))
        #self.payload.status.update(dict)
