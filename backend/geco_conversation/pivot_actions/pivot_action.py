from geco_conversation import *
from workflow.pivot import Pivot
class PivotAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        #self.context.workflow.run(self.context.workflow[0])
        self.context.add_bot_msgs([Utils.chat_message(messages.pivot_message)])
        self.context.add_bot_msgs([Utils.chat_message('Do you want features or samples in the rows?')])
        return None, False

    def logic(self, message, intent, entities):
        self.context.payload.back = PivotAction
        from geco_conversation.new_dataset import NewDataset
        if ('metadata_row' not in self.status) and ('region_row' not in self.status):
            if message.lower() in  ['feature','features']:
                self.context.add_bot_msgs([Utils.chat_message(messages.row_region_message),
                                           Utils.choice('Available regions', {i:i for i in self.context.payload.database.region_schema})])
                return RegionRow(self.context), False
            elif message.lower() in  ['sample','samples']:
                #self.context.add_bot_msgs([Utils.chat_message(messages.row_meta_message)])
                self.context.add_bot_msgs([Utils.chat_message("I will put 'item_id' in the rows, ok?")])
                return MetaRow(self.context), False
            else:
                self.context.add_bot_msg(Utils.chat_message('Sorry I did not understand. Features or samples?'))
                return None, False

        elif 'region_value' not in self.status:

            value = message
            self.context.payload.insert('region_value', [value])
            return Labels(self.context), True


        return None, False


class RegionRow(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if 'region_row' not in self.status:
            region_row = message
            self.context.payload.insert('region_row', [region_row])
            self.context.add_bot_msg(Utils.chat_message('I will put in the columns \'item_id\', ok?'))
            return None, False
        else:
            meta_column = 'item_id'
            self.context.payload.insert('meta_column', [meta_column])
            self.context.add_bot_msgs([Utils.chat_message(messages.value_region_message),Utils.choice('Available regions', {i:i for i in self.context.payload.database.region_schema})])

            return PivotAction(self.context), False


class MetaRow(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if 'meta_row' not in self.status:
            meta_row = 'item_id'
            self.context.payload.insert('metadata_row', [meta_row])
            self.context.add_bot_msg(Utils.chat_message(messages.column_region_message))
            return None, False

        else:
            region_column = message
            self.context.payload.insert('region_column', [region_column])
            self.context.add_bot_msgs([Utils.chat_message(messages.value_region_message),
                                       Utils.choice('Available regions',
                                                    {i: i for i in self.context.payload.database.region_schema})])

            return PivotAction(self.context), False

class Labels(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.add_bot_msg(Utils.chat_message('Do you want to add some labels from metadata or region data?'))
        return None, False

    def logic(self, message, intent, entities):
        if intent!='deny' and 'other_meta' not in self.status:
                self.context.payload.insert('other_meta',None)
                self.context.add_bot_msg(Utils.chat_message('Do you want to add a label to the samples? Choose one in the right pane'))
                return MetaLabels(self.context), False
        if intent!='deny' and 'other_region' not in self.status:
            others = message.split(';')
            self.context.payload.insert('other_region', others)
            print(others)
        #elif 'other_region' not in self.status:
         #   self.context.payload.insert('other_region', None)

        if 'region_row' in self.status:
            if 'other_region' in self.status and self.status['other_meta']!=[None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],other_meta=self.status['other_meta'],other_region=self.status['other_region']))
            elif 'other_region' in self.status:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],other_region=self.status['other_region']))
            elif self.status['other_meta'] != [None]:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value'],
                                                other_meta=self.status['other_meta']))
            else:
                self.context.workflow.add(Pivot(self.context.workflow[-1], region_row=self.status['region_row'],
                                                metadata_column=['item_id'], region_value=self.status['region_value']))

        elif 'metadata_row' in self.status:
            if 'other_region' in self.status and self.status['other_meta']!=[None]:
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
            elif self.status['other_meta'] != [None]:
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
        self.context.workflow.run(self.context.workflow[-1])
        self.context.add_bot_msgs([Utils.chat_message(messages.other_dataset),
                                   Utils.table_viz('Pivot', self.context.workflow[-1].result)])
        # print(Utils.table_viz('Pivot',self.context.workflow[-1].result))
        self.context.payload.clear()
        return NewDataset(self.context), False

class MetaLabels(AbstractAction):
    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent!='deny':
            others = message.split(';')
            self.context.payload.update('other_meta', others)
            print(others)
            self.context.add_bot_msg(
                Utils.chat_message('Do you want to add a label to the features? Choose one in the right pane'))
        return Labels(self.context), False


