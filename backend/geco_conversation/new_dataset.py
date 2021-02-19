from geco_conversation import *

class NewDataset(AbstractAction):
    def help_message(self):
        return []

    def on_enter(self):
        for i in self.context.data_extraction.datasets:
            gcm = {x: i.fields[x] for x in i.fields if x != 'metadata'}
            if 'metadata' in i.fields:
                meta = {x: i.fields['metadata'][x] for x in i.fields['metadata']}
            else:
                meta ={}
            donors = self.context.payload.database.retrieve_donors(gcm, meta)
            if len(set(self.table[self.table['donor_source_id'] in donors]['dataset_name'].values))>=2:
                self.context.payload.insert('donors',donors)
                self.context.add_bot_msgs([Utils.chat_message('The datasets on the right contain different data for the same patients that you selected. '
                                                              'Do you want also one of these datasets?')])
                return SameDonorDataset(self.context), False
        self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
        return None, False

    def logic(self, message, intent, entities):
        from geco_conversation.gmql_actions.gmql_unary_action import GMQLUnaryAction
        from geco_conversation.gmql_actions.gmql_binary_action import GMQLBinaryAction
        if intent=='affirm':
            return StartAction(self.context), True
        elif intent=='deny':
            if self.context.payload.back != PivotAction:
                if len(self.context.data_extraction.datasets)%2==0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
                else:
                    return PivotAction(self.context), True
            else:
                return DataAnalysis(self.context), True
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.not_understood)])
            return None, False

class SameDonorDataset(AbstractAction):
    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from geco_conversation import PivotAction
        if intent!='deny':
            if intent!='affirm':
                self.context.payload.insert('dataset_name',message)
                gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
                links = self.context.payload.database.download(gcm_filter, self.status['donors'])
                self.context.add_bot_msgs([Utils.chat_message(messages.download),
                                           Utils.workflow('Data Selection', download=True, link_list=links),
                                           Utils.chat_message(messages.gmql_operations), Utils.param_list(gcm_filter)])
                if len(self.context.data_extraction.datasets) % 2 == 0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context),
                                       GMQLBinaryAction(self.context)), False
                else:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), PivotAction(self.context)), False