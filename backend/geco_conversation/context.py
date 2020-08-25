from geco_conversation import StartAction


class Step:
    # Manca delta context
    def __init__(self, logic, user_msg = None, bot_msgs = None):
        self.logic = logic  #forse TUPLA (node, logic)
        self.bot_msgs = bot_msgs,
        self.user_msg = user_msg

class Context:


    def __init__(self):

        self.history = []

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


