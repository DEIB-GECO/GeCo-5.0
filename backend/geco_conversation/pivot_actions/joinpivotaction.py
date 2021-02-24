from geco_conversation import *

class JoinPivotAction(AbstractAction):
	def help_message(self):
		self.context.add_bot_msgs([Utils.chat_message(helpMessages.join_pivot_help)])
		return None, True

	def on_enter(self):
		self.context.add_bot_msg("Do you want to choose a joinby value?\nIf so, tell me which one.")
		return None, False

	def logic(self,message, intent, entities):

		if intent!='deny':
			self.context.add_bot_msg("Ok, I will join the two tables according to {}.\nDo you want to select another dataset?")

		else:
			self.context.add_bot_msg("Ok, I will do the cartesian product of the two tables.")

		return YesNoAction(self.context, NewDataset(self.context), DataAnalysis(self.context)), False