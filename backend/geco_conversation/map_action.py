from geco_conversation import *
class MapAction(AbstractAction):
	def  help_message(self):
		pass

	def on_enter(self):
		ds_1 = self.context.data_extraction.datasets[-2].name
		ds_2 = self.context.data_extraction.datasets[-1].name
		self.context.add_bot_msg(Utils.chat_message("I will use {} as a reference to operate on {}. Do you confirm or you want to switch the two datasets?".format(ds_1,ds_2)))
		return None, False

	def logic(self,message, intent, entities):
		ds_1 = self.context.data_extraction.datasets[-2]
		ds_2 = self.context.data_extraction.datasets[-1]
		if intent=='affirm':
			self.context.payload.insert('map',{'ds_ref':ds_1.name, 'ds_exp':ds_2.name})
			self.context.add_bot_msg(Utils.chat_message("Do you want to put any equality constraint on one or more metadata? If so, tell me which ones (separate them by ';')."))
		else:
			self.context.payload.insert('map', {'ds_ref': ds_2.name, 'ds_exp': ds_1.name})
			self.context.add_bot_msg(Utils.chat_message("Do you want to put any equality constraint on one or more metadata? If so, tell me which ones (separate them by ';')."))
		return MapS2Action(self.context), False

class MapS2Action(AbstractAction):
	def  help_message(self):
		pass

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):
		if intent != 'deny':
			values = message.lower().strip().split(';')
			values = [Field(v) for v in values]
			self.context.insert('joinby', values)
		self.context.add_bot_msg(Utils.chat_message("By default I will count the overlapping regions between the reference and the experiments datasets. I will name the count value \"count_map\".\nDo you want to rename it? In case, please digit the new name."))
		return MapS3Action(self.context), False

class MapS3Action(AbstractAction):
	def  help_message(self):
		pass

	def on_enter(self):
		pass

	def logic(self,message, intent, entities):
		if intent!='deny':
			self.context.payload.insert('count_name',message)
		else:
			self.context.payload.insert('count_name', 'count_map')
		return MapS4Action(self.context), True

class MapS4Action(AbstractAction):
	def  help_message(self):
		pass

	def on_enter(self):
		self.context.add_bot_msg(Utils.chat_message("Do you want to add other aggregation functions? If so, tell me which one."))
		return None, False


	def logic(self,message, intent, entities):
		from .gmql_unary_action import GMQLUnaryAction
		from .gmql_binary_action import GMQLBinaryAction
		if intent!='deny':
			if 'aggregate' not in self.status:
				self.context.payload.insert('aggregate', message)
			else:
				self.context.payload.update('aggregate', message)
			self.context.add_bot_msg(Utils.chat_message("Do you want to add other aggregation functions? If so, tell me which one."))
			return None, False
		else:
			depends_on_2 = None
			for i in range(len(self.context.workflow), 0):
				if isinstance(self.context.workflow[i], Select):
					print(self.context.workflow[i - 1])
					depends_on_2 = self.context.workflow[i - 1]
					break
			print(depends_on_2)
			if 'aggregate' in self.status and 'joinby' in self.status:
				self.context.workflow.add(Map(self.context.workflow[-1], depends_on_2, joinby=self.status['joinby'], name_agg=self.status['count_name'], other_aggregates= self.status['aggregate']))
			elif 'joinby' in self.status:
				self.context.workflow.add(Map(self.context.workflow[-1], depends_on_2, joinby=self.status['joinby'],
												  name_agg=self.status['count_name']))
			else:
				self.context.workflow.add(Map(self.context.workflow[-1], depends_on_2,
											  name_agg=self.status['count_name']))

			self.context.add_bot_msg(Utils.chat_message("Do you want to modify the new dataset?"))
			return YesNoAction(self.context, GMQLUnaryAction(self.context), NewDataset(self.context)), False
