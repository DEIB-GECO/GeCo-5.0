from geco_conversation import *
from data_structure.dataset import Dataset

class NewDataset(AbstractAction):
    def help_message(self):
        return []

    def on_enter(self):
        table = self.context.payload.database.table
        num_tables = 0
        ds_list = []
        print('donors',len(self.status['donors']))
        for ds in set(table['dataset_name']):
            common_donors = set(table[(table['donor_source_id'].isin(self.status['donors'])) & ((table['dataset_name'] == ds))]['donor_source_id'].values)
            self.context.payload.insert('common_donors', {ds: common_donors})
            print('common', len(common_donors))
            if (len(common_donors) / len(self.status['donors'])) > 0.75:
                num_tables += 1
                ds_list.append(ds)
        if num_tables >= 2:
            self.context.add_bot_msgs([Utils.chat_message(
                'The datasets on the right contain different data for at least 75% of the patients that you selected. '
                'Do you want also one of these datasets?'),
                                       Utils.choice('Datasets', {i: i for i in ds_list})])
            return SameDonorDataset(self.context), False
        self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
        return None, False

    def logic(self, message, intent, entities):
        from geco_conversation.gmql_actions.gmql_unary_action import GMQLUnaryAction
        from geco_conversation.gmql_actions.gmql_binary_action import GMQLBinaryAction
        if intent == 'affirm':
            self.context.add_bot_msg(Utils.workflow('Data Selection 2'))
            return StartAction(self.context), True
        elif intent == 'deny':
            if self.context.payload.back != PivotAction:
                if len(self.context.data_extraction.datasets) % 2 == 0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context),
                                       GMQLBinaryAction(self.context)), False
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
        from geco_conversation import GMQLUnaryAction, GMQLBinaryAction
        if intent != 'deny':
            if intent != 'affirm':
                self.context.payload.insert('dataset_name', message)
                gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
                self.context.payload.database.update(gcm_filter)
                print(set(self.context.payload.database.table['dataset_name'].values))
                links = self.context.payload.database.download(gcm_filter, self.status['common_donors'])
                ds = Dataset(gcm_filter, 'DS_'+str(len(self.context.data_extraction.datasets) +1 ), donors=self.status['common_donors'])
                self.context.data_extraction.datasets.append(ds)
                self.context.add_bot_msgs([Utils.chat_message(messages.download),Utils.workflow('Data Selection'),
                                           Utils.workflow('Data Selection', download=True, link_list=links),
                                           Utils.chat_message(messages.gmql_operations), Utils.param_list(gcm_filter), Utils.tools_setup(add=[], remove=["available_choices"])])
                if len(self.context.data_extraction.datasets) % 2 == 0:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context),
                                       GMQLBinaryAction(self.context)), False
                else:
                    return YesNoAction(self.context, GMQLUnaryAction(self.context), PivotAction(self.context)), False
            elif intent == 'affirm':
                self.context.add_bot_msgs([Utils.chat_message(
                    'Which one do you want?'),
                    Utils.choice('Datasets', {i: i for i in list(set(
                        self.context.payload.database.table[
                            self.context.payload.database.table['donor_source_id'].isin(self.status['donors'])][
                            'dataset_name'].values))})])
                return None, False
        else:
            self.context.payload.delete('common_donors')
            self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
            return NewDataset(self.context), False