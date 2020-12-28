from geco_conversation import *

class JoinPivotAction(AbstractAction):
	def on_enter(self):
		self.context.add_bot_msg("Do you want to choose a joinby value?\nIf so, tell me which one.")

	def logic(self,message, intent, entities):

		if intent!='deny':
			self.context.add_bot_msg("Ok, I will join the two tables according to {}.\nDo you want to select another dataset?")

		else:
			self.context.add_bot_msg("Ok, I will do the cartesian product of the two tables.")

		return YesNoAction(self.context, NewDataset(self.context), DataAnalysis(self.context)), False