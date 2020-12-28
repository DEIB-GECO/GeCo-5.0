from geco_conversation import *

class UnionAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.union_help)])

    def on_enter(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.rename)])
        return None, False

    def logic(self, message, intent, entities):
        names = {}
        for i in range(len(self.context.data_extraction.datasets)):
            names["DS_" + str(i)] = self.context.data_extraction.datasets[i].name

        if intent != "deny":
            name = message.strip()
        else:
            name = "DS_" + str(len(self.context.data_extraction.datasets) +1 )
        names['Union']=name
        print(len(self.context.workflow))
        for i in range(len(self.context.workflow)-1,0,-1):
            print(self.context.workflow[i].__class__.__name__)
            if self.context.workflow[i].__class__.__name__=='Select':
                depends_on_2 = self.context.workflow[i-1]
                break
        self.context.workflow.add(Union(self.context.workflow[-1], depends_on_2))
        self.context.add_bot_msgs([Utils.chat_message(messages.named.format(name)),
                Utils.chat_message(messages.other_dataset), Utils.param_list(names)])
        return YesNoAction(self.context, StartAction(self.context), PivotAction(self.context)), False
