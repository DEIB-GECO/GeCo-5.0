from geco_conversation import *

class MapAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent != 'deny':
            self.status['joinby'] = message
            for i in range(len(self.context.workflow), 0):
                if self.context.workflow[i].__class__.__name__ == 'Select':
                    depends_on_2 = self.context.workflow[i - 1]
                    break
            self.context.workflow.add(Map(self.context.workflow[-1], depends_on_2, joinby=self.status['joinby']))
        else:
            for i in range(len(self.context.workflow), 0):
                if self.context.workflow[i].__class__.__name__ == 'Select':
                    depends_on_2 = self.context.workflow[i - 1]
                    break
            self.context.workflow.add(Map(self.context.workflow[-1], depends_on_2, joinby=self.status['joinby']))
        # names = {}
        # for i in range(len(self.context.data_extraction.datasets)):
        #     names["DS_" + str(i)] = self.context.data_extraction.datasets[i].name
        #
        # if intent != "deny":
        #     name = message.strip()
        # else:
        #     name = "DS_" + str(len(self.context.data_extraction.datasets) + 1)
        # names['Map'] = name

        self.context.add_bot_msg(Utils.chat_message('Do you want to do another operation on this dataset?'))
        return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
