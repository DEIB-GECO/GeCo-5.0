from geco_conversation import *
from workflow.pivot import Pivot
class PivotAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(messages.union_help)]

    def on_enter(self):
        self.context.workflow.run(self.context.workflow[0])
        self.context.add_bot_msgs([Utils.chat_message(messages.pivot_message)])
        self.context.add_bot_msgs([Utils.chat_message(messages.row_message)])
        return None, False

    def logic(self, message, intent, entities):
        self.context.workflow.add(Pivot(self.context.workflow[-1], meta_column='gene_symbol', region_row='biospecimen_aliquot__bcr_sample_barcode', region_value='rpkm'))
        self.context.workflow.run(self.context.workflow[-1])
        self.context.add_bot_msgs([Utils.chat_message('Sorry not implemented yet')])
        return None, False