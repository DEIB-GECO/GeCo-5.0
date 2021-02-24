from geco_conversation import *

class JoinAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.join_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from geco_conversation.gmql_actions.gmql_unary_action import GMQLUnaryAction

        if intent != 'deny':
            self.payload.insert('joinby',Field(message))
            for i in range(len(self.context.workflow), 0):
                if self.context.workflow[i].__class__.__name__ == 'Select':
                    depends_on_2 = self.context.workflow[i - 1]
                    self.context.workflow.add(
                        Join(self.context.workflow[-1], depends_on_2, joinby=self.status['joinby']))
                    break

        else:
            for i in range(len(self.context.workflow), 0):
                if self.context.workflow[i].__class__.__name__ == 'Select':
                    depends_on_2 = self.context.workflow[i - 1]
                    self.context.workflow.add(Join(self.context.workflow[-1], depends_on_2))
                    break

        # names = {}
        # for i in range(len(self.context.data_extraction.datasets)):
        #     names["DS_" + str(i)] = self.context.data_extraction.datasets[i].name
        #
        # if intent != "deny":
        #     name = message.strip()
        # else:
        #     name = "DS_" + str(len(self.context.data_extraction.datasets) + 1)
        # names['Join'] = name

        self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
        #self.context.payload.clear()
        return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False

