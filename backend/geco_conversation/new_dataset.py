from geco_conversation import *
from data_structure.dataset import Dataset
from data_structure.database import DB, fields, datasets
import copy
import pandas as pd


class NewDataset(AbstractAction):
    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.new_dataset_help)])
        return None, True

    def on_enter(self):
        table = self.context.payload.database.table
        num_tables = 0
        len_donors = len(self.context.data_extraction.datasets[-1].donors)
        print('donors', len(set(self.context.data_extraction.datasets[-1].donors)))
        self.context.payload.insert('common_donors', {})
        for d in self.context.data_extraction.datasets:
            print(d.fields['dataset_name'])
        for ds in datasets:
            for d in self.context.data_extraction.datasets:
                if d.fields['dataset_name'] != [ds]:
                    common_donors = set(table[(table['donor_source_id'].isin(
                        list(set(self.context.data_extraction.datasets[-1].donors)))) & (
                                                  (table['dataset_name'] == ds))]['donor_source_id'].values)
                    self.context.payload.update('common_donors', {ds: common_donors})
                    print('common', len(common_donors))
                    if (len(common_donors) / len_donors) > 0.75:
                        num_tables += 1

        if num_tables >= 2:
            self.context.add_bot_msgs([Utils.chat_message(
                'The datasets on the right contain different data for some of the patients that you selected before. You can see the percentage of the common patients for each dataset.'
                'Do you want also one of these datasets?'),
                Utils.choice('Datasets', {f'{k}: {round((len(v) / len_donors) * 100, 2)}%': k for k, v in
                                          self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0}),
                Utils.tools_setup(add=None, remove='data_summary'), Utils.tools_setup(add=None, remove='table')])
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


class DonorDataset(AbstractAction):
    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.new_dataset_help)])
        return None, True

    def on_enter(self):
        table = self.context.payload.database.table
        num_tables = 0
        len_donors = len(self.context.data_extraction.datasets[-1].donors)
        print('donors', len(set(self.context.data_extraction.datasets[-1].donors)))
        self.context.payload.insert('common_donors', {})
        for d in self.context.data_extraction.datasets:
            print(d.fields['dataset_name'])
        for ds in set(table['dataset_name']):
            for d in self.context.data_extraction.datasets:
                if d.fields['dataset_name'] != [ds]:
                    common_donors = set(table[(table['donor_source_id'].isin(
                        list(set(self.context.data_extraction.datasets[-1].donors)))) & (
                                                  (table['dataset_name'] == ds))]['donor_source_id'].values)
                    self.context.payload.update('common_donors', {ds: common_donors})
                    print('common', len(common_donors))
                    if (len(common_donors) / len_donors) > 0.75:
                        num_tables += 1

        if num_tables >= 2:
            table = pd.DataFrame(index=self.status['common_donors'].keys())
            table['Number of Donors'] = [len(set(v)) for k, v in self.status['common_donors'].items() if
                                         (len(v) / len_donors) * 100 > 0]
            table['Common Percentage'] = [{round((len(v) / len_donors) * 100, 2)} for k, v in
                                          self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0]
            self.context.add_bot_msgs([Utils.chat_message(
                'The datasets on the right contain different data for some of the patients that you selected before. You can see the percentage of the common patients for each dataset.'
                'Do you want also one of these datasets?'),
                Utils.choice('Datasets', {f'{k}: {round((len(v) / len_donors) * 100, 2)}%': k for k, v in
                                          self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0}),Utils.table_viz(table),
                Utils.tools_setup(add=None, remove='data_summary'), Utils.tools_setup(add=None, remove='table')])
            return SameDonorDataset(self.context), False

        return DataAnalysis(self.context), True

    def logic(self, message, intent, entities):
        table = self.context.payload.database.table
        num_tables = 0
        len_donors = len(self.context.data_extraction.datasets[-1].donors)
        print('donors', len(set(self.context.data_extraction.datasets[-1].donors)))
        self.context.payload.insert('common_donors', {})
        for d in self.context.data_extraction.datasets:
            print(d.fields['dataset_name'])
        for ds in set(table['dataset_name']):
            for d in self.context.data_extraction.datasets:
                if d.fields['dataset_name'] != [ds]:
                    common_donors = set(table[(table['donor_source_id'].isin(
                        list(set(self.context.data_extraction.datasets[-1].donors)))) & (
                                                  (table['dataset_name'] == ds))]['donor_source_id'].values)
                    self.context.payload.update('common_donors', {ds: common_donors})
                    print('common', len(common_donors))
                    if (len(common_donors) / len_donors) > 0.75:
                        num_tables += 1

        if num_tables >= 2:
            table = pd.DataFrame(index= self.status['common_donors'].keys())
            table['Number of Donors'] =  [len(set(v)) for k,v in self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0]
            table['Common Percentage'] = [{round((len(v) / len_donors) * 100, 2)} for k, v in
                                          self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0]
            self.context.add_bot_msgs([Utils.chat_message(
                'The datasets on the right contain different data for some of the patients that you selected before. You can see the percentage of the common patients for each dataset.'),
                Utils.chat_message(
                    'Do you want also one of these datasets? If not, you will proceed with the analysis.'),
                Utils.choice('Datasets', {f'{k}: {round((len(v) / len_donors) * 100, 2)}%': k for k, v in
                                          self.status['common_donors'].items() if (len(v) / len_donors) * 100 > 0}),Utils.table_viz(table),
                Utils.tools_setup(add=None, remove='data_summary'), Utils.tools_setup(add=None, remove='table')])
            return SameDonorDataset(self.context), False

        return DataAnalysis(self.context), True


class SameDonorDataset(AbstractAction):
    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.same_donor_help)])
        return None, False

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        from geco_conversation import PivotAction
        from geco_conversation import GMQLUnaryAction, GMQLBinaryAction
        if intent != 'deny':
            print('intent not deny')
            del self.context.payload.database
            self.context.payload.database = DB(fields, False, copy.deepcopy(self.context.payload.original_db))
            if intent != 'affirm':
                print('intent not affirm')
                self.context.payload.insert('dataset_name', message)
                gcm_filter = {k: v for (k, v) in self.status.items() if k in self.context.payload.database.fields}
                self.context.payload.database.update(gcm_filter)
                name = 'DS_' + str(len(self.context.data_extraction.datasets) + 1)
                self.context.payload.insert('fields', {'dataset_name': message, 'name': name})
                print(set(self.context.payload.database.table['dataset_name'].values))
                links = self.context.payload.database.download(gcm_filter, self.status['common_donors'])
                self.context.payload.database.update({})
                ds = Dataset(gcm_filter, name,
                             donors=self.status['common_donors'])
                self.context.data_extraction.datasets.append(ds)
                self.context.add_bot_msgs([Utils.chat_message(messages.download), Utils.workflow('Data Selection 2'),
                                           Utils.workflow('Data Selection 2', download=True, link_list=links),
                                           Utils.param_list(gcm_filter),
                                           Utils.tools_setup(add=[], remove="available_choices")])
                regions = self.context.payload.database.find_regions(gcm_filter, {})

                # self.context.add_bot_msgs([Utils.chat_message(messages.gmql_operations)])
                # if len(self.context.data_extraction.datasets) % 2 == 0:
                #   return YesNoAction(self.context, GMQLUnaryAction(self.context),
                #                       GMQLBinaryAction(self.context)), False
                # else:
                #    return YesNoAction(self.context, GMQLUnaryAction(self.context), PivotAction(self.context)), False
                return RegionAction(self.context), True
            else:
                print('intent affirm')
                self.context.add_bot_msgs([Utils.chat_message(
                    'Which one do you want?'),
                    Utils.choice('Datasets', {k: k for k, v in self.status['common_donors'].items() if
                                              (len(v) / len(list(set(self.status['donors'])))) * 100 > 0})])
                return None, False
        else:
            self.context.payload.delete('common_donors')
            # self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
            # return NewDataset(self.context), False
            return DataAnalysis(self.context), True
