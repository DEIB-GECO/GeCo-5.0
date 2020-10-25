class Delta:
    def insert_value(self, name):
        if hasattr(self, 'insertion'):
            self.insertion.append(name)
        else:
            self.insertion = [name]

    def delete_value(self, name, value):
        if hasattr(self, 'deletion'):
            self.deletion.append({'variable': name, 'value': value})
        else:
            self.deletion = [{'variable': name, 'value': value}]

    def update_value(self, name, old_value, new_value):
        if hasattr(self, 'update'):
            self.update.append({'variable': name, 'new': new_value, 'old': old_value})
        else:
            self.update = [{'variable': name, 'new': new_value, 'old': old_value}]

class Step:
    def __init__(self, bot_msgs, action= None, user_msg = None):
        self.action = action
        self.bot_msgs = bot_msgs
        self.user_msg = user_msg
        self.delta = Delta()

class Payload:
    def __init__(self, context):
        self.context = context
        self.status = {}

    def insert(self, key, value):
        if isinstance(value, list) or isinstance(value, dict):
            self.status[key]=value
        else:
            self.status[key] = [value]
        self.context.top_delta().insert_value(key)

    def update(self, key, new_value):
        old = self.status[key]
        if isinstance(old, list):
            self.status[key].append(new_value)
        elif isinstance(old, dict):
            self.status[key].update(new_value)
        self.context.top_delta().update_value(key, old, self.status[key])

    def replace(self, key, new):
        old = self.status[key]
        self.status[key] = new
        if old!=new:
            self.context.top_delta().update_value(key, old, self.status[key])

    def delete(self, key, value=None):
        if value==None:
            del (self.status[key])
            self.context.top_delta().delete_value(key, value)
        elif self.status[key]==value:
            del(self.status[key])
            self.context.top_delta().delete_value(key, value)
        else:
            old = self.status[key].copy()
            self.status[key] = old.remove(value)
            self.context.top_delta().update_value(key, old, self.status[key])

    def clear(self):
        for x in self.status:
            self.context.top_delta().delete_value(x, self.status[x])
        self.status.clear()

class Data_Extraction:
    def __init__(self):
        self.datasets = []
        self.binary = []
        self.unary = []
        self.table = {}

class Operation:
    def __init__(self, type, name, dict):
        self.type = type
        self.name = name
        self.parameters = dict

class Workflow(list):
    def __init__(self):
        self = []

    def add_gmql(self, name, dict):
        self.append((Operation('gmql', name, dict), False))

    def add_pivot(self, name, dict):
        self.append((Operation('pivot', name, dict), False))

    def add_analysis(self, name, dict):
        self.append((Operation('analysis', name, dict), False))

    def run(self):
        #run logic
        pass

class Context:
    def __init__(self):
        self.history = []
        self.payload = Payload(self)
        self.workflow = Workflow()
        self.data_extraction = Data_Extraction()
        '''
        self.data_analysis = {
            'par_tuning' : [],
            'validation' : [],
            'algorithms' : []
        }
        '''

    def add_step(self, bot_msgs = None, action = None, user_msg = None):
        self.history.append(Step(bot_msgs, action, user_msg))

    def top_bot_msgs(self):
        if (self.history[-1].bot_msgs != None):
            return self.history[-1].bot_msgs
        elif (len(self.history) >= 2) and (self.history[-2].bot_msgs!=None):
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
        print()
        if type(self.history[-1].bot_msgs)== list:
            self.history[-1].bot_msgs.append(bot_msg)
        elif self.history[-1].bot_msgs==None:
            self.history[-1].bot_msgs = [bot_msg]
        else:
            self.history[-1].bot_msgs = [self.history[-1].bot_msgs, bot_msg]

    def add_bot_msgs(self, bot_msgs):
        if (self.history[-1].bot_msgs!=None):
            if isinstance(self.history[-1].bot_msgs, list):
                self.history[-1].bot_msgs.extend(bot_msgs)
            else:
                self.history[-1].bot_msgs=[self.history[-1].bot_msgs].extend(bot_msgs)
        else:
            self.history[-1].bot_msgs = bot_msgs

    def add_delta(self, delta):
        self.history[-1].delta = delta

    def pop(self):
        del (self.history[-1])
        self.revert()
        action = self.history[-1].action
        del (self.history[-1])
        self.add_step(action=action)
        #self.history[-2].bot_msgs = None

    def last_valid_user_msg(self):
        return self.history[-1].user_msg

    def revert(self):
        if hasattr(self.history[-1].delta, 'insertion'):
            for i in self.history[-1].delta.insertion:
                del (self.payload.status[i])

        if hasattr(self.history[-1].delta, 'deletion'):
            for elem in self.history[-1].delta.deletion:
                self.payload.status[elem['variable']]=elem['value']

        if hasattr(self.history[-1].delta, 'update'):
            for elem in self.history[-1].delta.update:
                self.payload.status[elem['variable']]=elem['new_value']

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
        self.payload.status.update(dict)


