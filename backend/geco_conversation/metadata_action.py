from database import experiment_fields
import messages
from geco_conversation import *

class MetadataAction(AbstractAction):

    def on_enter_messages(self):
        return [Utils.chat_message("You can also select samples with specific conditions. Do you want to filter on metadata?")], None, {}

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        if intent == 'affirm':
            self.status['fields'].update({'metadata':{}})
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name','metadata']}

            keys = self.status['geno_surf'].find_all_keys(gcm_filter)
            self.available_keys = {x.replace('_', ' '): x for x in keys if keys[x] > 1}

            if len(self.available_keys) > 1:
                self.logic = self.key_logic
                return [Utils.chat_message("Which metadatum do you want to filter on?"),
                        Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                     helpIconContent=messages.fields_help),
                        Utils.param_list(self.status['fields'])], None, {}
            elif len(self.available_keys) == 1:
                values, number = self.status['geno_surf'].find_key_values(gcm_filter, self.available_keys.keys[0])
                if number == False:
                    list_param = {x['value']: x['value'] for x in values}
                    self.logic = self.value_string_logic
                    return [Utils.chat_message(
                        "Which value do you want to select?\nIf you want more, please separate them using ';'."),
                            Utils.choice('Available values', list_param, show_help=True,
                                         helpIconContent=messages.fields_help),
                            Utils.param_list(self.status['fields'])], \
                           None, {}
                else:
                    self.logic = self.value_number_logic
                    print('CIAO')
                    return [Utils.chat_message(
                        "Which range of values do you want? You can tell me the minimum or maximum value or both.\nThe values are shown in the histogram."),
                               Utils.param_list(self.status['fields'])], \
                           None, {}
            else:
                back = MetadataAction
                return [], Confirm(
                    {"geno_surf": self.status['geno_surf'], "fields": self.status['fields'], "back": back}), {}

        elif intent == 'deny':
            back = MetadataAction
            return [], Confirm(
                {"geno_surf": self.status['geno_surf'], "fields": self.status['fields'], "back": back}), {}


    def metadata_logic(self, message, intent, entities):
        from .confirm import Confirm
        if intent=='affirm':
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k != 'name' and k!='metadata'}
            meta_filter = {k: v for (k,v) in self.status['fields']['metadata'].items()}
            keys = self.status['geno_surf'].find_all_keys(gcm_filter, meta_filter)
            self.available_keys = {x.replace('_', ' '): x for x in keys if keys[x] > 1}
            print(self.available_keys)
            if len(self.available_keys) > 1:
                self.logic = self.key_logic
                return [Utils.chat_message("Which metadatum do you want to filter on?"),
                        Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                     helpIconContent=messages.fields_help),
                        Utils.param_list(self.status['fields'])], None, {}
            elif len(self.available_keys) == 1:
                gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name','metadata']}
                meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}
                self.status['fields']['metadata'].update({self.available_keys.keys[0]: []})
                values, number = self.status['geno_surf'].find_key_values(self.available_keys.keys[0], gcm_filter, meta_filter)
                if number == False:
                    list_param = {x['value']: x['value'] for x in values}
                    self.logic = self.value_string_logic
                    return [Utils.chat_message("Which value do you want to select?\nIf you want more, please separate them using ';'."),
                            Utils.choice('Available values', list_param, show_help=True,
                                         helpIconContent=messages.fields_help),
                            Utils.param_list(self.status['fields'])], \
                           None, {}
                else:
                    self.logic = self.value_number_logic
                    print('CIAO')
                    return [Utils.chat_message(
                        "Which range of values do you want? You can tell me the minimum or maximum value or both.\nThe values are shown in the histogram."),
                               Utils.param_list(self.status['fields'])], \
                           None, {}
            else:
                back = MetadataAction
                return [Utils.chat_message('I\'m sorry.\nThere are no more metadata to filter on.')], Confirm({"geno_surf": self.status['geno_surf'], "fields": self.status['fields'], "back": back}), {}

        elif intent=='deny':
            back = MetadataAction
            return [],  Confirm({"geno_surf": self.status['geno_surf'], "fields": self.status['fields'], "back": back}), {}



    def key_logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k != 'name' and k != 'metadata'}
        meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}

        k =  message.lower().strip()
        if k.replace('_', ' ') in self.available_keys:
            self.selected_key = k
            self.status['fields']['metadata'].update({self.selected_key:[]})
            values, number = self.status['geno_surf'].find_key_values(str(k), gcm_filter, meta_filter)
            self.available_values = [val['value'] for val in values]
            #print(values)
            if number==False:
                list_param = {x: x for x in self.available_values}
                self.logic = self.value_string_logic
                return [Utils.chat_message("Which value do you want to select?"),
                        Utils.choice('Available values',list_param, show_help=True, helpIconContent=messages.fields_help),
                        Utils.param_list(self.status['fields'])], \
                       None, {}
            else:
                self.logic = self.value_number_logic
                return [Utils.chat_message("Which range of values do you want? You can see the values in the histogram."),
                        Utils.param_list(self.status['fields'])], \
                       None, {}

        return [], None, {}

    def value_string_logic(self, message, intent, entities):
        values = message.lower().strip().split(';')
        print(values)
        not_present = []
        for v in values:
            v=v.strip()
            if v in self.available_values:
                self.status['fields']['metadata'][self.selected_key].append(v)
            else:
                not_present.append(v)
        if len(self.status['fields']['metadata'][self.selected_key])==0:
            del(self.status['fields']['metadata'][self.selected_key])
        #self.status['fields']['metadata'].update({self.status['selected_key']: self.status[self.status['selected_key']]})
        if not_present==[]:
            self.logic=self.metadata_logic
            return [Utils.chat_message("Ok, the chosen values are shown in the bottom right pane."),
                    Utils.chat_message("Do you want to filter on other metadata?"),
                    Utils.param_list(self.status['fields'])], None, {}
        else:
            if not_present==values:
                del(self.status[self.status['selected_key']])
            self.logic = self.metadata_logic
            return [Utils.chat_message("You selected {}, not present in the choices.\nThe other choices are in the bottom right pane.".format(",".join(i for i in not_present))),
                    Utils.chat_message("Do you want to filter on other metadata?")],\
                   None, {}

    def value_number_logic(self, message, intent, entities):
        v = message.lower().strip()
        if v in self.available_values:
            self.status['fields']['metadata'][self.selected_key].append(v)
            return [Utils.chat_message("Ok, you selected {}".format(v)),
                    Utils.param_list(self.status['fields'])], None, {}
        else:
            self.logic = self.metadata_logic
            return [Utils.chat_message("You selected {}, not present in the choices".format(v)),
                    Utils.chat_message("Do you want to filter on other metadata?"),
                    Utils.param_list(self.status['fields'])], None, {}
