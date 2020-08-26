from geco_conversation import StartAction


class Step:
    # Manca delta context
    def __init__(self, bot_msgs, logic = None, user_msg = None):
        self.logic = logic  #forse TUPLA (node, logic)
        self.bot_msgs = bot_msgs,
        self.user_msg = user_msg

class Context:


    def __init__(self):

        self.history = []

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

    def add_step(self, bot_msgs, logic = None, user_msg = None):
        self.history.append(Step(bot_msgs, logic, user_msg))

    def top_bot_msgs(self):
        return self.history[-1].bot_msgs

    def add_user_msg(self, user_msg):
        self.history[-1].user_msg = user_msg
