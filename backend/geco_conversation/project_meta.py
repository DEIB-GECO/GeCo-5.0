from geco_conversation import *
from data_structure.operations import ArithmeticOperation

class ProjectMetaAction(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("We are beginning a Project operation, to create a new metadatum or modifying an existing one.\n"
													"Write the name of an existing metadatum, if you want to modify its values,"
													" or tell me a new name for the metadatum you want to create."))
		return None, False

	def logic(self,message, intent, entities):
		from .gmql_unary_action import GMQLUnaryAction
		from .gmql_binary_action import GMQLBinaryAction
		self.context.payload.insert('back', ProjectMetaAction)
		self.context.payload.insert('project_meta', {'name': Field(message)})
		if self.context.data_extraction.datasets[-1].meta_schema!=None and message in self.context.data_extraction.datasets[-1].meta_schema:
			self.context.add_bot_msg(Utils.chat_message("You are going to modify {}.\n"
														"If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label').\n"
														"If you want to compute its value starting from an existing metadata, please tell me the metadatum name.".format(message)))
		else:
			self.context.add_bot_msg(Utils.chat_message("You are creating {} metadatum.\n"
														"If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label').\n"
														"If you want to compute its value starting from an existing metadata, please tell me the metadatum name.".format(message)))
		return ProjectMetaS2Action(self.context), False

class ProjectMetaS2Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):
		if message.isnumeric():
			self.context.payload.update('project_meta', {'value': message})
			return ProjectMetaS5Action(self.context), True
		else:
			self.context.payload.update('project_meta', {'op1': Field(message)})
			self.context.add_bot_msg(Utils.chat_message("Which operation do you want to do?"))
			return ProjectMetaS3Action(self.context), False


class ProjectMetaS3Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):

		if message=='+':
			new = {'operation': ArithmeticOperation.SUM.parameters(op1=self.status['project_meta']['op1'])}
			self.context.payload.update('project_meta', new)
			print(self.status['project_meta'])
			self.context.add_bot_msg(Utils.chat_message("Please, insert the value or the metadatum you want to add"))
			return ProjectMetaS4Action(self.context), False
		elif message=='-':
			new = {'operation': ArithmeticOperation.SUBTRACT.parameters(op1=self.status['project_meta']['op1'])}
			self.context.payload.update('project_meta', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the value or the metadatum you want to subtract"))
			return ProjectMetaS4Action(self.context), False
		elif message=='*':
			new = {'operation': ArithmeticOperation.PRODUCT.parameters(op1=self.status['project_meta']['op1'])}
			self.context.payload.update('project_meta', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the factor.\nIt can be either a value or a metadatum."))
			return ProjectMetaS4Action(self.context), False
		elif message=='/':
			new = {'operation': ArithmeticOperation.DIVISION.parameters(op1=self.status['project_meta']['op1'])}
			self.context.payload.update('project_meta', new)
			self.context.add_bot_msg(Utils.chat_message("Please, insert the divider.\nIt can be either a value or a metadatum."))
			return ProjectMetaS4Action(self.context), False
		else :
			self.context.add_bot_msg(Utils.chat_message("Sorry, I didn't understand.\nCan you choose among the ones on the right?"))
			return None, False

class ProjectMetaS4Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		pass
	def logic(self,message, intent, entities):
		if message.isnumeric():
			new = {
				'operation': self.status['project_meta']['operation'].parameters(op1=self.status['project_meta']['op1'],
																				 op2=float(message))}
			self.context.payload.update('project_meta', new)
		else:
			new = {'operation': self.status['project_meta']['operation'].parameters(
				op1=self.status['project_meta']['op1'], op2=Field(message))}
			self.context.payload.update('project_meta', new)
		return ProjectMetaS5Action(self.context), True

class ProjectMetaS5Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("Do you want to confirm your choices?"))
		return None, False

	def logic(self,message, intent, entities):
		if intent!='deny':
			return ProjectMetaS6Action(self.context), True
		else:
			self.context.payload.delete('project_meta', self.status['project_meta'])
			self.context.add_bot_msg(Utils.chat_message("We restart the project.\nTell me the metadatum to modify or the new metadatum you want to add."))
			return ProjectMetaAction(self.context), False

class ProjectMetaS6Action(AbstractAction):
	def help_message(self):
		return []

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("Do you want to add/modify other metadata?\nIf so, tell me which one or the name of the new one."))
		return None, False

	def logic(self,message, intent, entities):
		from .gmql_unary_action import GMQLUnaryAction
		from .gmql_binary_action import GMQLBinaryAction
		if intent!='deny':
			return ProjectMetaAction(self.context), False
		else:
			change_dict = {self.status['project_meta']['name']: self.status['project_meta']['operation']}
			self.context.workflow.add(ProjectMetadata(self.context.workflow[-1], change_dict=change_dict))
			self.context.add_bot_msg(Utils.chat_message(messages.new_gmql_operation))
			self.context.payload.clear()

			if len(self.context.data_extraction.datasets) % 2 == 0:
				return YesNoAction(self.context, GMQLUnaryAction(self.context), GMQLBinaryAction(self.context)), False
			else:
				return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
