from get_api import annotation_fields, check_existance
import messages
from geco_conversation import *


class AnnotationAction(AbstractAction):

    def on_enter_messages(self):
        return self.logic(None, None, None)

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf']

    def create_piecharts(self, gcm_filter):
        msgs = []
        msgs.append(Utils.tools_setup('dataviz','dataset'))
        values = {}
        if 'content_type' not in self.status:
            content_type_val = self.status['geno_surf'].retrieve_values(gcm_filter, 'content_type')
            values['Content Type'] = content_type_val
        if 'assembly' not in self.status:
            assembly_val = self.status['geno_surf'].retrieve_values(gcm_filter, 'assembly')
            values['Assembly'] = assembly_val
        source_val = self.status['geno_surf'].retrieve_values(gcm_filter, 'source')
        values['Source'] = source_val
        msgs.append(Utils.pie_chart(values))
        return msgs


    def logic(self, message, intent, entities):
        from .confirm import Confirm

        for field in annotation_fields:
            if field in self.status and len(self.status[field]) > 1:
                self.status[field] = self.status[field][:1]

        gcm_filter = {k: v for (k, v) in self.status.items() if k in annotation_fields}
        print(gcm_filter)
        self.status['geno_surf'].update(gcm_filter)
        pie_charts = self.create_piecharts(gcm_filter)
        Utils.pyconsole_debug(self.status)

        if message is None:
            if "content_type" not in self.status:
                db = self.status['geno_surf'].content_type_db
                list_param = {x: x for x in self.status['geno_surf'].content_type_db}
                return [Utils.chat_message("Please provide a content (annotation) type"),
                        Utils.choice("content_type", list_param)] + pie_charts, \
                       None, {}
            elif "assembly" not in self.status:
                list_param = {x: x for x in self.status['geno_surf'].assembly_db}
                return [Utils.chat_message("Please provide an assembly"),
                        Utils.choice("assembly", list_param)] + pie_charts, \
                       None, {}
            elif "source" not in self.status:
                if len(self.status['geno_surf'].source_db)>1:
                    list_param = {x: x for x in self.status['geno_surf'].source_db}
                    return [Utils.chat_message("Please provide a source"),
                            Utils.choice("source", list_param)] + pie_charts, \
                           None, {}
                else:
                    self.status['source'] = self.status['geno_surf'].source_db
        else:
            if "content_type" not in self.status:
                content_type = entities['content_type'] if "content_type" in entities else [message.strip().lower()]
                if content_type[0] not in self.status["geno_surf"].content_type_db:
                    list_param = {x: x for x in self.status['geno_surf'].content_type_db}
                    return [Utils.chat_message("Content type {} not valid, insert a valid one".format(content_type)),
                            Utils.choice("content_type", list_param)] + pie_charts, \
                           None, {}
                else:
                    self.status['content_type'] = content_type
                    pie_charts = self.create_piecharts(gcm_filter)
                    list_param = {x: self.status[x] for x in annotation_fields if x in self.status}
                    msg, nx, delta = self.logic(None, None, None)
                    return [Utils.param_list(list_param)] + msg + pie_charts, nx, delta

            elif "assembly" not in self.status:
                assembly = entities['assembly'] if "assembly" in entities else [message.strip().lower()]
                if assembly[0] not in self.status["geno_surf"].assembly_db:
                    db = self.status["geno_surf"].assembly_db
                    list_param = {x: x for x in self.status['geno_surf'].assembly_db}
                    return [Utils.chat_message("Assembly {} not valid, insert a valid one".format(assembly)),
                            Utils.choice("assembly", list_param)] + pie_charts, \
                           None, {}
                else:
                    self.status['assembly'] = assembly
                    pie_charts = self.create_piecharts(gcm_filter)
                    list_param = {x: self.status[x] for x in annotation_fields if x in self.status}
                    msg, nx, delta = self.logic(None, None, None)
                    return [Utils.param_list(list_param)] + msg + pie_charts, nx, delta

            elif "source" not in self.status:
                source = entities['source'] if "source" in entities else [message.strip().lower()]
                if source[0] not in self.status["geno_surf"].source_db:
                    list_param = {x: x for x in self.status['geno_surf'].source_db}
                    return [Utils.chat_message("Source {} not valid, insert a valid one".format(source)),
                            Utils.choice("source", list_param)] + pie_charts, \
                           None, {}
                else:
                    self.status['source'] = source
                    pie_charts = self.create_piecharts(gcm_filter)
                    list_param = {x: self.status[x] for x in annotation_fields if x in self.status}
                    msg, nx, delta = self.logic(None, None, None)
                    return [Utils.param_list(list_param)] + msg + pie_charts, nx, delta

        fields = {x: self.status[x] for x in annotation_fields}
        samples = check_existance(True, fields)

        back = AnnotationAction

        if samples > 0:
            return [Utils.param_list(fields)], Confirm({"geno_surf": self.status['geno_surf'], "fields": fields, "back": back}), {}
        else:
            for a in annotation_fields:
                del self.status[a]
            return [Utils.param_list(fields),Utils.chat_message(messages.no_ann_found)], self, {}

