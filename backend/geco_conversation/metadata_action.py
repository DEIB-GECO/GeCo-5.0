from get_api import experiment_fields
import messages
import numpy as np
import time
from geco_conversation import *

class MetadataAction(AbstractAction):

    def on_enter_messages(self):
        return self.logic(None, None, None)

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']


    def logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status['fields']}
        #self.status['geno_surf'].update(gcm_filter)

        keys = self.status['geno_surf'].find_keys(gcm_filter, '%')
        if message is None:
            list_param = {x: x for x in keys}
            #self.logic = self.field_logic
            return [Utils.chat_message("Which key do you want to filter on?"),
                    Utils.choice('Available keys',list_param, show_help=True, helpIconContent=messages.fields_help),
                    Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})], \
                   None, {}

        return [], None, {}
