from geco_conversation import *
from data_structure.operations import ArithmeticOperation

class ProjectRegionAction(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("We are beginning a Project operation, to create a new region  or modifying an existing one.\n"
													"Write the name of an existing region , if you want to modify its values,"
													" or tell me a new name for the region  you want to create."))

	def logic(self,message, intent, entities):
		self.context.payload.insert('back', ProjectRegionAction)
		self.context.payload.insert('project_region', {'name': Field(message)})
		if self.context.data_extraction.datasets[-1].region_schema!=None and message in self.context.data_extraction.datasets[-1].region_schema:
			self.context.add_bot_msg(Utils.chat_message("You are going to modify {}.\n"
														"If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label').\n"
														"If you want to compute its value starting from an existing region , please tell me the region  name.".format(message)))
		else:
			self.context.add_bot_msg(Utils.chat_message("You are creating {} region .\n"
														"If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label').\n"
														"If you want to compute its value starting from an existing region , please tell me the region  name.".format(message)))
		return ProjectRegionS2Action(self.context), False

class ProjectRegionS2Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):
		if message.isnumeric():
			self.context.payload.update('project_region', {'value': message})
			return ProjectRegionS5Action(self.context), True
		else:
			self.context.payload.update('project_region', {'op1': Field(message)})
			self.context.add_bot_msg(Utils.chat_message("Which operation do you want to do?"))
			return ProjectRegionS3Action(self.context), False


class ProjectRegionS3Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):

		if message=='+':
			new = {'operation': ArithmeticOperation.SUM.parameters(op1=self.status['project_region']['op1'])}
			self.context.payload.update('project_region', new)
			print(self.status['project_region'])
			self.context.add_bot_msg(Utils.chat_message("Please, insert the value or the region  you want to add"))
			return ProjectRegionS4Action(self.context), False
		elif message=='-':
			new = {'operation': ArithmeticOperation.SUBTRACT.parameters(op1=self.status['project_region']['op1'])}
			self.context.payload.update('project_region', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the value or the region  you want to subtract"))
			return ProjectRegionS4Action(self.context), False
		elif message=='*':
			new = {'operation': ArithmeticOperation.PRODUCT.parameters(op1=self.status['project_region']['op1'])}
			self.context.payload.update('project_region', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the factor.\nIt can be either a value or a region ."))
			return ProjectRegionS4Action(self.context), False
		elif message=='/':
			new = {'operation': ArithmeticOperation.DIVISION.parameters(op1=self.status['project_region']['op1'])}
			self.context.payload.update('project_region', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the divider.\nIt can be either a value or a region ."))
			return ProjectRegionS4Action(self.context), False
		else :
			self.context.add_bot_msg(Utils.chat_message("Sorry, I didn't understand.\nCan you choose among the ones on the right?"))
			return None, False

class ProjectRegionS4Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass
	def logic(self,message, intent, entities):
		if message.isnumeric():
			new = {
				'operation': self.status['project_region']['operation'].parameters(op1=self.status['project_region']['op1'],
																				 op2=float(message))}
			self.context.payload.update('project_region', new)
		else:
			new = {'operation': self.status['project_region']['operation'].parameters(
				op1=self.status['project_region']['op1'], op2=Field(message))}
			self.context.payload.update('project_region', new)
		return ProjectRegionS5Action(self.context), True

class ProjectRegionS5Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("Do you want to confirm your choices?"))
		return None, False

	def logic(self,message, intent, entities):
		if intent!='deny':
			return ProjectRegionS6Action(self.context), True
		else:
			self.context.payload.delete('project_region', self.status['project_region'])
			self.context.add_bot_msg(Utils.chat_message("We restart the project.\nTell me the region  to modify or the new region  you want to add."))
			return ProjectRegionAction(self.context), False

class ProjectRegionS6Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("Do you want to add/modify other region ?\nIf so, tell me which one or the name of the new one."))
		return None, False

	def logic(self,message, intent, entities):
		from geco_conversation.gmql_actions.gmql_unary_action import GMQLUnaryAction
		from geco_conversation.gmql_actions.gmql_binary_action import GMQLBinaryAction
		if intent!='deny':
			return ProjectRegionAction(self.context), False
		else:
			change_dict = {self.status['project_region']['name']: self.status['project_region']['operation']}
			self.context.workflow.add(ProjectRegion(self.context.workflow[-1], change_dict=change_dict))
			self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
			self.context.payload.clear()

			if len(self.context.data_extraction.datasets) % 2 == 0:
				return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
			else:
				return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
