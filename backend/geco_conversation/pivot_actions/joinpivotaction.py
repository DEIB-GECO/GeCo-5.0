from geco_conversation import *

class JoinPivotAction(AbstractAction):
	def help_message(self):
		self.context.add_bot_msgs([Utils.chat_message(helpMessages.join_pivot_help)])
		return None, True

	def on_enter(self):
		print('HEREEEE JOINNNNNNNN')
		#self.context.add_bot_msg("Do you want to choose a joinby value?\nIf so, tell me which one.")
		self.context.add_bot_msg(Utils.chat_message("Do you want to join the two tables?"))
		return JoinPivotAction(self.context), False

	def logic(self,message, intent, entities):
		from geco_conversation.data_analysis.data_analysis import DataAnalysis
		if intent!='deny':
			#self.context.add_bot_msg(Utils.chat_message("Ok, I will join the two tables. It will take some times, at the end you will see the result on the right."))
			print(len(self.context.workflow))
			for i in range((len(self.context.workflow)-2), 0, -1):
				print(i)
				print(self.context.workflow[i].__class__.__name__)
				if self.context.workflow[i].__class__.__name__ == 'Pivot':
					depends_on_2 = self.context.workflow[i]
					self.context.workflow.add(
						JoinPivot(self.context.workflow[-1], depends_on_2))#, joinby=self.status['joinby']))
					break
			self.context.workflow.run(self.context.workflow[-1],self.context.session_id)
			self.context.add_bot_msgs([Utils.chat_message(
				"Ok, I joined the two tables. The result is on the right."),Utils.table_viz( self.context.workflow[-1].result)])

			return DataAnalysis(self.context), True
		else:
			#self.context.add_bot_msg("Ok, I will do the cartesian product of the two tables.")
			self.context.add_bot_msg(Utils.chat_message(messages.other_dataset))

		return YesNoAction(self.context, NewDataset(self.context), DataAnalysis(self.context)), False