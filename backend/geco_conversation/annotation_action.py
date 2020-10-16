from data_structure.database import annotation_fields
from geco_conversation import *

class AnnotationAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.annotation_help)])
        return None, False

    def logic(self, message, intent, entities):
        from .askconfirm import AskConfirm
        self.context.payload.back = AnnotationAction

        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in annotation_fields:
                self.status[k] = [x for x in v if x in getattr(self.context.payload.database, str(k) + '_db')]
                if len(self.status[k]) == 0:
                    del (self.status[k])

        gcm_filter = {k: v for (k, v) in self.status.items() if k in annotation_fields}

        if len(gcm_filter) > 0:
            self.context.payload.database.update(gcm_filter)

        #pie_charts = Utils.create_piecharts(self.context,gcm_filter)

        missing_fields = self.context.payload.database.fields_names
        list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
        samples = self.context.payload.database.check_existance(gcm_filter)

        if samples > 0:
            #if message is None:
            #list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
            if len(list_param)!=0:
                self.context.add_bot_msgs([Utils.chat_message("Which field do you want to select?"),
                        Utils.choice('Available fields', list_param, show_help=True, helpIconContent=helpMessages.fields_help),
                        Utils.param_list({k:v for (k,v) in self.status.items() if k in annotation_fields})] + Utils.create_piecharts(self.context,gcm_filter))
                return FieldAction(self.context), False
            else:
                fields = {x: self.status[x] for x in annotation_fields if x in self.status}
                self.status.clear()
                self.status['fields'] = fields
                self.context.add_bot_msgs([Utils.param_list(self.status['fields'])])
                return AskConfirm(self.context), True

        else:
            for x in annotation_fields:
                if x in self.status:
                    del self.status[x]
            self.context.add_bot_msgs([Utils.param_list(gcm_filter), Utils.chat_message(messages.no_exp_found)])
            return None, False