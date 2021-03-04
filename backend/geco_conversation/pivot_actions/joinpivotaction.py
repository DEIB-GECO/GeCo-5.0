from geco_conversation import *

class JoinPivotAction(AbstractAction):
	def help_message(self):
		self.context.add_bot_msgs([Utils.chat_message(helpMessages.join_pivot_help)])
		return None, True

	def on_enter(self):
		#self.context.add_bot_msg("Do you want to choose a joinby value?\nIf so, tell me which one.")
		self.context.add_bot_msg(Utils.chat_message("Do you want to join the two tables?"))
		return None, False

	def logic(self,message, intent, entities):

		if intent!='deny':
			#self.context.add_bot_msg("Ok, I will join the two tables according to {}.\nDo you want to select another dataset?")
			self.context.add_bot_msg(Utils.chat_message(
				"Ok, I will join the two tables. It will take some times, at the end you will see the result on the right."))
			for i in range(len(self.context.workflow), 0):
				if self.context.workflow[i].__class__.__name__ == 'Pivot':
					depends_on_2 = self.context.workflow[i]
					self.context.workflow.add(
						JoinPivot(self.context.workflow[-1], depends_on_2))#, joinby=self.status['joinby']))
					break
			self.context.workflow.run(self.context.workflow[-1])
			return DataAnalysis(self.context), False
		else:
			#self.context.add_bot_msg("Ok, I will do the cartesian product of the two tables.")
			self.context.add_bot_msg(Utils.chat_message(messages.other_dataset))

		return YesNoAction(self.context, NewDataset(self.context), DataAnalysis(self.context)), False