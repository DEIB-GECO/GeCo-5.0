from geco_conversation import *
from workflow.pivot import Pivot
class PivotAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.workflow.run(self.context.workflow[0])
        self.context.add_bot_msgs([Utils.chat_message(messages.pivot_message)])
        self.context.add_bot_msgs([Utils.chat_message(messages.row_meta_message)])
        return None, False

    def logic(self, message, intent, entities):
        if 'metadata_row' not in self.status and 'region_row' not in self.status:
            meta_row = Field(message)
            self.context.payload.insert('metadata_row', [meta_row])
            self.context.add_bot_msg(Utils.chat_message(messages.column_region_message))
            return None, False
        elif 'region_column' not in self.status:
            reg_col = Field(message)
            self.context.payload.insert('region_column', [reg_col])
            self.context.add_bot_msg(Utils.chat_message(messages.value_region_message))
            return None, False
        elif 'region_value' not in self.status:
            value = Field(message)
            self.context.payload.insert('region_value', [value])
            self.context.add_bot_msg(Utils.chat_message(messages.value_region_message))
            self.context.workflow.add(
                Pivot(self.context.workflow[-1], region_column=self.status['region_column'], metadata_row=self.status['metadata_row'], region_value=value))
            self.context.workflow.run(self.context.workflow[-1])
            self.context.add_bot_msgs([Utils.chat_message('Sorry not implemented yet')])
            self.context.payload.clear()
            return None, False
       # self.context.workflow.add(Pivot(self.context.workflow[-1], meta_column=['gene_symbol'],
         #                               region_row=['biospecimen_aliquot__bcr_sample_barcode'], region_value='rpkm'))
        return None, False