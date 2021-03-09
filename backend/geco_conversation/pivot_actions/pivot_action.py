from geco_conversation import *
from workflow.pivot import Pivot


class PivotAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.pivot_help)])
        return None, True

    def on_enter(self):
        # self.context.workflow.run(self.context.workflow[0])
        self.context.add_bot_msgs([Utils.chat_message(messages.pivot_message)])
        self.context.add_bot_msgs([Utils.chat_message('According to what you want to analyze, I\'ll build your table. '
                                                      'Do you want to do operations on the features (e.g. genes) or on the samples?'),
                                   Utils.choice('Rows', {'Features': 'features', 'Samples': 'samples'})])
        self.context.add_bot_msgs([Utils.workflow('Pivot')])
        return None, False

    def logic(self, message, intent, entities):
        self.context.payload.back = PivotAction

        if ('metadata_row' not in self.status) and ('region_row' not in self.status):
            if message.lower() in ['feature', 'features', 'regions', 'region data', 'region'] or intent == 'feature':
                if self.context.payload.database.region_schema != None:
                    reg_row = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
                    self.context.add_bot_msgs([Utils.chat_message(messages.row_region_message),
                                               Utils.choice('Available regions', reg_row)])
                    return RegionRow(self.context), False
                else:
                    self.context.add_bot_msgs([Utils.chat_message(messages.regions_not_available)])
                    self.context.add_bot_msg(
                        Utils.chat_message("Do you want to start again from the beginning?"))
                    return ByeAction(self.context), False
            elif message.lower() in ['sample', 'samples'] or intent == 'sample':
                meta_row = 'item_id'
                reg_row = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
                self.context.payload.insert('metadata_row', [meta_row])
                # self.context.add_bot_msgs([Utils.chat_message(messages.row_meta_message)])
                # self.context.add_bot_msgs([Utils.chat_message("I will put 'item_id' in the rows, ok?")])
                return MetaRow(self.context), True
            else:
                self.context.add_bot_msg(Utils.chat_message('Sorry I did not understand. Features or samples?'))
                return None, False

        elif 'region_value' not in self.status:

            value = message.strip()
            if value not in self.context.payload.database.region_schema:
                self.context.add_bot_msgs(
                    [Utils.chat_message("Sorry, your choice is not correct. Please, choose one in the right panel."),
                     Utils.choice('Available regions',
                                  {i: i for i in self.context.payload.database.region_schema
                                   if
                                   i != 'item_id'})])
                return None, False
            self.context.payload.insert('region_value', [value])
            return Labels(self.context), True

        return None, False


class RegionRow(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        node, bool = self.logic(None, None, None)
        return node, bool

    def logic(self, message, intent, entities):
        if 'region_row' not in self.status:
            region_row = message.strip().split(',')
            for r in region_row:
                if r not in self.context.payload.database.region_schema:
                    reg_row = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
                    self.context.add_bot_msgs([Utils.chat_message(
                        "Sorry, your choice is not correct. Please, choose one in the right panel."),
                                               Utils.choice('Available regions', reg_row)])
                    return None, False
            self.context.payload.insert('region_row', region_row)
            # self.context.add_bot_msg(Utils.chat_message('I will put in the columns \'item_id\', ok?'))
            # return None, True
            # else:
            meta_column = 'item_id'
            self.context.payload.insert('meta_column', [meta_column])
            self.context.add_bot_msgs([Utils.chat_message(messages.value_region_message),
                                       Utils.choice('Available regions',
                                                    {i: i for i in self.context.payload.database.region_schema if
                                                     i != 'item_id'})])

            return PivotAction(self.context), False


class MetaRow(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        if 'metadata_row' not in self.status:
            meta_row = 'item_id'
            self.context.payload.insert('metadata_row', [meta_row])
            reg_row = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
            self.context.add_bot_msg(Utils.chat_message(messages.column_region_message))
            self.context.add_bot_msgs([Utils.choice('Available regions', reg_row)])
            return None, False
        else:
            reg_row = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
            self.context.add_bot_msg(Utils.chat_message(messages.column_region_message))
            self.context.add_bot_msgs([Utils.choice('Available regions', reg_row)])
            return None, False

    def logic(self, message, intent, entities):
        if 'metadata_row' not in self.status:
            meta_row = 'item_id'
            self.context.payload.insert('metadata_row', [meta_row])
            self.context.add_bot_msg(Utils.chat_message(messages.column_region_message))
            return None, False

        else:
            region_column = message.strip().split(',')
            print(region_column)
            for r in region_column:
                if r not in self.context.payload.database.region_schema:
                    reg_col = {'chrom,start,stop': 'chrom,start,stop', 'gene_symbol': 'gene_symbol'}
                    self.context.add_bot_msgs([Utils.chat_message(
                        "Sorry, your choice is not correct. Please, choose one in the right panel."),
                                               Utils.choice('Available regions', reg_col)])
                    return None, False
            self.context.payload.insert('region_column', region_column)
            self.context.add_bot_msgs([Utils.chat_message(messages.value_region_message),
                                       Utils.choice('Available regions',
                                                    {i: i for i in self.context.payload.database.region_schema if
                                                     i != 'item_id'})])

            return PivotAction(self.context), False


class Labels(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.add_bot_msg(Utils.choice('',{}))
        self.context.add_bot_msg(Utils.chat_message('Do you want to add some labels from metadata or region data?'))
        return None, False

    def logic(self, message, intent, entities):
        from geco_conversation.new_dataset import DonorDataset
        if intent != 'deny' and 'other_meta' not in self.status:
            self.context.payload.insert('other_meta', None)
            self.context.add_bot_msg(
                Utils.chat_message('Do you want to add a label to the samples? Choose one in the right pane'))
            if hasattr(self.context.payload.database, 'metadata'):
                keys = list(set(self.context.payload.database.metadata['key'].values))
                self.context.add_bot_msg(Utils.choice('Metadata', {i: i for i in keys}, show_search=True))
            return MetaLabels(self.context), False
        if intent != 'deny' and 'other_region' not in self.status:
            others = message.split(';')
            self.context.payload.insert('other_region', others)

        if 'region_row' in self.status:
            if 'other_region' in self.status and self.status['other_meta'] != [None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],
                                                other_meta=self.status['other_meta'],
                                                other_region=self.status['other_region']))
            elif 'other_region' in self.status:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],
                                                other_region=self.status['other_region']))
            elif 'other_meta' in self.status and self.status['other_meta'] != [None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],
                                                other_meta=self.status['other_meta']))
            else:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value']))

        elif 'metadata_row' in self.status:
            if 'other_region' in self.status and self.status['other_meta'] != [None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], metadata_row=['item_id'],
                                                region_column=self.status['region_column'],
                                                region_value=self.status['region_value'],
                                                other_meta=self.status['other_meta'],
                                                other_region=self.status['other_region']))
            elif 'other_region' in self.status:
                self.context.workflow.add(Pivot(self.context.workflow[-1], metadata_row=['item_id'],
                                                region_column=self.status['region_column'],
                                                region_value=self.status['region_value'],
                                                other_region=self.status['other_region']))
            elif 'other_meta' in self.status and self.status['other_meta'] != [None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], metadata_row=['item_id'],
                                                region_column=self.status['region_column'],
                                                region_value=self.status['region_value'],
                                                other_meta=self.status['other_meta']))
            else:
                self.context.workflow.add(Pivot(self.context.workflow[-1], metadata_row=['item_id'],
                                                region_column=self.status['region_column'],
                                                region_value=self.status['region_value']))

        # self.context.workflow.add(
        #    Pivot(self.context.workflow[-1], region_column=self.status['region_column'], metadata_row=self.status['metadata_row'], region_value=value))
        if len(self.context.data_extraction.datasets) == 1:
            self.context.workflow.run(self.context.workflow[-1], self.context.session_id)
            self.context.add_bot_msgs([Utils.chat_message(
                'On the right, if you click on "Table", you can see the table. You can download it. Is it ok?'),
                                       Utils.table_viz('Table', self.context.workflow[-1].result.ds),
                                       Utils.tools_setup(add=None, remove='pie-chart')])
        else:
            # self.context.workflow.write_workflow()
            # with open('workflow.txt','r') as f:
            #    workflow = f.readlines()
            # self.context.add_bot_msgs([Utils.chat_message('I am sorry but for now you can download only the workflow you did'), Utils.workflow('Download', download=True)])
            self.context.workflow.run(self.context.workflow[-1],self.context.session_id)
            self.context.add_bot_msgs([Utils.chat_message(
                'On the right, if you click on "Table", you can see the table. You can download it. Is it ok?'),
                Utils.table_viz('Table', self.context.workflow[-1].result.ds),
                Utils.tools_setup(add=None, remove='data_summary')])

        # self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset)])
        # print(Utils.table_viz('Pivot',self.context.workflow[-1].result))
        self.context.payload.clear()
        print(len(self.context.data_extraction.datasets))
        if len(self.context.data_extraction.datasets) == 2:
            return JoinPivotAction(self.context), True
        return YesNoAction(self.context, DonorDataset(self.context),ChangePivot(self.context)), False


class MetaLabels(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent != 'deny':
            others = message.split(';')
            self.context.payload.update('other_meta', others)
            print(others)
            self.context.add_bot_msg(
                Utils.chat_message('Do you want to add a label to the features? Choose one in the right pane'))
            # self.context.add_bot_msg(Utils.choice('Regions',{i: i for i in self.context.payload.database.region_schema if
            #                                        i != 'item_id'}))
            self.context.add_bot_msg(Utils.choice('Available regions',
                                                  {i: i for i in self.context.payload.database.region_schema if
                                                   i != 'item_id'}))
        return Labels(self.context), False

class ChangePivot(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.payload.back = ChangePivot
        self.context.add_bot_msg(
            Utils.chat_message('Do you want to transpose the table?'))
        return None, False

    def logic(self, message, intent, entities):
        from geco_conversation.new_dataset import DonorDataset
        if self.context.payload.back == ChangePivot:
            if intent == 'affirm':
                self.context.workflow[-1].result.ds = self.ds.T
                self.context.add_bot_msgs([Utils.chat_message(
                    'On the right, if you click on "Table", you can see the table. You can download it. Is it ok?'),
                    Utils.table_viz('Table', self.context.workflow[-1].result.ds[:100].T[:100].T)])
                return YesNoAction(self.context, DonorDataset(self.context),ChangePivot(self.context)), False
            else:
                self.context.payload.back == PivotAction
                self.context.add_bot_msg(
                    Utils.chat_message('Do you want to change the value in the table?'))
                return None, False
        else:
            if intent=='affirm':
                self.context.payload.delete('region_value')
                self.context.add_bot_msgs([Utils.chat_message(messages.value_region_message),
                                           Utils.choice('Available regions',
                                                        {i: i for i in self.context.payload.database.region_schema if
                                                         i != 'item_id'})])
                return PivotAction(self.context), False
