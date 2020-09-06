from geco_conversation import StartAction

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
    # Manca delta context
    def __init__(self, bot_msgs, node= None, logic = None, user_msg = None):
        self.node = node
        self.logic = logic  #forse TUPLA (node, logic)
        self.bot_msgs = bot_msgs
        self.user_msg = user_msg
        self.delta = Delta()

class Payload:
    def __init__(self):
        self.status = {}

class Context:

    def __init__(self):

        self.history = []

        self.payload = Payload()
        '''
        self.data_extraction = {
            'datasets' : [],
            'binary' : [],
            'unary' : [],
            'table' : []
        }

        self.data_analysis = {
            'par_tuning' : [],
            'validation' : [],
            'algorithms' : []
        }
        
        '''

    def add_step(self, bot_msgs = None, node = None, logic = None, user_msg = None):
        if logic == None:
            self.history.append(Step(bot_msgs, node, node.logic, user_msg))
        else:
            self.history.append(Step(bot_msgs, node, logic, user_msg))

    def top_bot_msgs(self):
        return self.history[-1].bot_msgs

    def top_user_msg(self):
        return self.history[-1].user_msg

    def top_logic(self):
        return self.history[-1].logic

    def top_node(self):
        return self.history[-1].node

    def top_delta(self):
        return self.history[-1].delta

    def add_user_msg(self, user_msg):
        self.history[-1].user_msg = user_msg

    def add_bot_msg(self, bot_msg):
        if type(self.history[-1].bot_msgs)== list:
            self.history[-1].bot_msgs.append(bot_msg)
        elif self.history[-1].bot_msgs==None:
            self.history[-1].bot_msgs = bot_msg
        else:
            self.history[-1].bot_msgs = [self.history[-1].bot_msgs, bot_msg]


    def add_bot_msgs(self, bot_msgs):
        if self.history[-1].bot_msgs!=None:
            if type(self.history[-1].bot_msgs)=='list':
                self.history[-1].bot_msgs.extend(bot_msgs)
            else:
                self.history[-1].bot_msgs=[self.history[-1].bot_msgs].extend(bot_msgs)
        else:
            self.history[-1].bot_msgs = bot_msgs

    def add_node(self, node):
        self.history[-1].node = node
        self.history[-1].logic = node.logic

    def add_logic(self, logic):
        self.history[-1].logic = logic

    def add_delta(self, delta):
        self.history[-1].delta = delta

    def pop(self):
        print('***CONTEXT***')
        for i in range(len(self.history)):
            print(i)
            print(self.history[i].node)
            print(self.history[i].logic)
        print('-----------------BEFORE------------------------')
        print(self.top_logic())
        print(self.top_node())
        del (self.history[-1])
        print('-----------------AFTER-------------------------')
        print(self.top_logic())
        print(self.top_node())
        self.revert()
        #elf.history[-1].node.status = self.history[-2].delta

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

        return

    def modify_status(self, dict):
        self.payload.status.update(dict)