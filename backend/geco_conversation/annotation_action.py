from data_structure.database import annotation_fields
from geco_conversation import *

class AnnotationAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.annotation_help)])
        return None, False

    def on_enter(self):
        node, bool = self.logic(None, None, None)
        return node, bool

    def check_status(self):
        temp = self.status.copy()
        for (k, v) in temp.items():
            if k in annotation_fields:
                self.context.payload.replace(k, [x for x in v if
                                                 x in self.context.payload.database.values[k]])
                if len(self.status[k]) == 0:
                    self.context.payload.delete(k)

    def filter(self, gcm_filter):
        if len(gcm_filter) > 0:
            self.context.payload.database.update(gcm_filter)

        samples = self.context.payload.database.check_existance(gcm_filter)

        return samples

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        self.context.payload.back = AnnotationAction
        self.check_status()
        gcm_filter = {k: v for (k, v) in self.status.items() if k in annotation_fields}
        samples = self.filter(gcm_filter)

        missing_fields = self.context.payload.database.fields_names
        list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}

        if samples > 0:
            if len(list_param)!=0:
                self.context.add_bot_msgs([Utils.chat_message("Which field do you want to select?"),
                        Utils.choice('Available fields', list_param, show_help=True, helpIconContent=helpMessages.fields_help),
                        Utils.param_list({k:v for (k,v) in self.status.items() if k in annotation_fields})] + Utils.create_piecharts(self.context,gcm_filter))
                return FieldAction(self.context), False
            else:
                fields = {x: self.status[x] for x in annotation_fields if x in self.status}
                self.context.payload.clear()
                self.context.payload.insert('fields', fields)
                self.context.add_bot_msgs([Utils.param_list(fields)])
                return RenameAction(self.context, MetadataAction(self.context)), True

        else:
            for x in annotation_fields:
                if x in self.status:
                    self.context.payload.delete(x)
            self.context.add_bot_msgs([Utils.chat_message(messages.no_exp_found)])
            return None, False