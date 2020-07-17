from database import experiment_fields
import messages
from geco_conversation import *

class MetadataAction(AbstractAction):

    def on_enter_messages(self):
        return self.logic(None, None, None)

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):
        print(self.status['fields'])
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k!='name'}
        #self.status['geno_surf'].update(gcm_filter)

        keys = self.status['geno_surf'].find_keys(gcm_filter, '%')
        self.available_keys = {x['key']: x['key'] for x in keys if x['count_values'] > 1}

        if message is None:

            if len(self.available_keys)>1:
                self.logic = self.key_logic
                return [Utils.chat_message("Which key do you want to filter on?"),
                        Utils.choice('Available keys',self.available_keys, show_help=True, helpIconContent=messages.fields_help),
                        Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})], \
                       None, {}
            elif len(self.available_keys)==1:
                values = self.status['geno_surf'].find_key_values(gcm_filter, self.available_keys.keys[0])
                list_param = {x['value']: x['value'] for x in values}
                self.logic = self.value_logic
                return [Utils.chat_message("Which value do you want to select?"),
                        Utils.choice('Available values', list_param, show_help=True,
                                     helpIconContent=messages.fields_help),
                        Utils.param_list({k: v for (k, v) in self.status.items() if k in experiment_fields})], \
                       None, {}
            else:
                return [Utils.chat_message(messages.bye_message)], None, {}

        return [], None, {}


    def value_logic(self, message, intent, entities):
        #gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'is_annotation']}
        v = message.lower().strip()
        print(self.available_values)
        if v in self.available_values:
            self.status[self.status['selected_key']] = v
            return [Utils.chat_message("Ok, you selected {}".format(v)),
                    Utils.param_list({k: v for (k, v) in self.status.items() if k in experiment_fields} + {
                        self.status['selected_key']: v})], None, {}
        return [], None, {}

    def key_logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name','is_annotation']}
        #self.status['geno_surf'].update(gcm_filter)
        #print(gcm_filter)
        k =  message.lower().strip()
        if k in self.available_keys:
            self.status['selected_key'] = k
            self.available_values = [val['value'] for val in self.status['geno_surf'].find_key_values(gcm_filter, k)]
            #print(values)
            list_param = {x['value']: x['value'] for x in self.available_values}
            self.logic = self.value_logic
            print('CIAO')
            return [Utils.chat_message("Which value do you want to select?"),
                    Utils.choice('Available values',list_param, show_help=True, helpIconContent=messages.fields_help),
                    Utils.param_list({k:v for (k,v) in self.status.items() if k in experiment_fields})], \
                   None, {}

        return [], None, {}

