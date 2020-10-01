from database import annotation_fields
import messages
from geco_conversation import *
from .field_action import FieldAction

class AnnotationAction(AbstractAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(messages.annotation_help)])
        return None, False

    def required_additional_status(self):
        return ['geno_surf']

    def create_piecharts(self, gcm_filter):
        msgs = []
        msgs.append(Utils.tools_setup('dataviz','dataset'))
        values = {}
        if 'content_type' not in self.status:
            content_type_val = self.context.payload.database.retrieve_values(gcm_filter, 'content_type')
            values['Content Type'] = content_type_val
        if 'assembly' not in self.status:
            assembly_val = self.context.payload.database.retrieve_values(gcm_filter, 'assembly')
            values['Assembly'] = assembly_val
        source_val = self.context.payload.database.retrieve_values(gcm_filter, 'source')
        values['Source'] = source_val
        msgs.append(Utils.pie_chart(values))
        return msgs

    def logic(self, message, intent, entities):
        from .confirm import Confirm
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
        pie_charts = self.create_piecharts(gcm_filter)
        # Find fields that are not already selected by the user
        missing_fields = self.context.payload.database.fields_names

        fields = {k: v for (k, v) in self.status.items() if k in annotation_fields}

        samples = self.context.payload.database.check_existance(fields)

        if samples > 0:
            if message is None:
                list_param = {x: x for x in list(set(missing_fields).difference(set(self.status.keys())))}
                if len(list_param)!=0:
                    #self.context.add_bot_msgs([Utils.chat_message("Which field do you want to select?"),
                     #       Utils.choice('Available fields',list_param, show_help=True, helpIconContent=messages.fields_help),
                     #       Utils.param_list({k:v for (k,v) in self.status.items() if k in annotation_fields})] + pie_charts)
                    self.context.add_bot_msgs([Utils.choice('Available fields',list_param, show_help=True, helpIconContent=messages.fields_help),
                            Utils.param_list({k:v for (k,v) in self.status.items() if k in annotation_fields})] + pie_charts)
                    self.context.payload.function = 'Field'
                    return FieldAction(self.context), False
                else:
                    fields = {x: self.status[x] for x in annotation_fields if x in self.status}
                    self.status.clear()
                    self.status['fields'] = fields
                    self.context.add_bot_msgs([Utils.param_list(self.status['fields'])])
                    return Confirm(self.context), True

        else:
            for x in annotation_fields:
                if x in self.status:
                    del self.status[x]
            self.context.add_bot_msgs([Utils.param_list(fields), Utils.chat_message(messages.no_exp_found)])
            return None, False