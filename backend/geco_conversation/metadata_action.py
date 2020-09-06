from database import experiment_fields
import re
import messages
from geco_conversation import *
import statistics

class MetadataAction(AbstractAction):

    def on_enter_messages(self):
        from .confirm import Confirm
        self.status['fields'].update({'metadata': {}})
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'metadata']}

        self.keys = self.status['geno_surf'].find_all_keys(gcm_filter)
        self.available_keys = {x.replace('_', ' '): x for x in self.keys if self.keys[x] > 1}
        #print(self.available_keys)
        if len(self.available_keys) >= 1:
            return [Utils.chat_message("You can also select samples with specific conditions. Do you want to filter on metadata?")], None, {}
        else:
            back = MetadataAction
            return [], Confirm({"geno_surf": self.status['geno_surf'], "fields": self.status['fields'], "back": back}), {}

    def help_message(self):
        return [Utils.chat_message(messages.annotation_help)]

    def required_additional_status(self):
        return ['geno_surf','dataset_list']

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        if intent == 'affirm':
            #self.status['fields'].update({'metadata':{}})
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name','metadata']}

            #keys = self.status['geno_surf'].find_all_keys(gcm_filter)
            #self.available_keys = {x.replace('_', ' '): x for x in keys if keys[x] > 1}

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

            list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
            list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                               self.status['fields']['metadata'] if self.status['fields']['metadata'][x]!=[]})

            if number==False:
                list_param = {x: x for x in self.available_values}
                self.logic = self.value_string_logic
                return [Utils.chat_message("Which value do you want to select?"),
                        Utils.choice('Available values',list_param, show_help=True, helpIconContent=messages.fields_help),
                        Utils.param_list(list_param)], \
                       None, {}
            else:
                numeric_values = [int(i) for i in self.available_values if i!=None]
                minimum = min(numeric_values)
                maximum = max(numeric_values)
                average = statistics.mean(numeric_values)
                list_param = {'min: {}'.format(minimum):minimum, 'max: {}'.format(maximum):maximum, 'mean: {}'.format(average):average}
                self.logic = self.value_number_logic
                return [Utils.chat_message("Which range of values do you want? You can see the values in the histogram."),
                        Utils.choice('Ranges',list_param, show_help=True, helpIconContent=messages.fields_help),Utils.param_list(self.status['fields'])], \
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

        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                       self.status['fields']['metadata']})

        if not_present==[]:
            self.logic=self.metadata_logic
            return [Utils.chat_message("Ok, the chosen values are shown in the bottom right pane."),
                    Utils.chat_message("Do you want to filter on other metadata?"),
                    Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                 helpIconContent=messages.fields_help),
                    Utils.param_list(list_param)], None, {}
        else:
            if not_present==values:
                del(self.status[self.status['selected_key']])
            self.logic = self.metadata_logic
            return [Utils.chat_message("You selected {}, not present in the choices.\nThe other choices are in the bottom right pane.".format(",".join(i for i in not_present))),
                    Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                 helpIconContent=messages.fields_help),
                    Utils.chat_message("Do you want to filter on other metadata?")],\
                   None, {}

    def value_number_logic(self, message, intent, entities):
        value_low = -99999999999999999999999999999999999999999999999999999
        value_high = 99999999999999999999999999999999999999999999999999999
        v = message.lower().strip()
        high = ['lower than', 'lower', 'smaller than', 'smaller', 'max is', 'max', 'maximum is', 'maximum', 'less than', 'less']
        low = ['higher than', 'higher', 'bigger than', 'bigger', 'min is', 'min', 'minimum is', 'minimum', 'more than', 'more']
        for l in high:
            if l in v:
                res = re.search(r'{0}\s*(\d+)'.format(re.escape(l)), message)
                value_high = int(res.group(1))
                print(value_high)
                break

        for h in low:
            if h in v:
                res = re.search(r'{0}\s*(\d+)'.format(re.escape(h)), message)
                value_low = int(res.group(1))
                print(value_low)
                break

        numeric_values = [int(i) for i in self.available_values if i!=None]
        print('VALUESSSSSS')
        print(numeric_values)
        for v in numeric_values:
            if (v>value_low) and (v<value_high):
                self.status['fields']['metadata'][self.selected_key].append(v)

        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x!='metadata'}
        list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in self.status['fields']['metadata']})

        if len(self.status['fields']['metadata'][self.selected_key])>0:
            self.logic = self.metadata_logic
            return [Utils.chat_message("Ok!"),Utils.chat_message("Do you want to filter on other metadata?"),
                    Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                 helpIconContent=messages.fields_help),
                    Utils.param_list(list_param)], None, {}
        else:
            self.logic = self.metadata_logic
            return [Utils.chat_message("There aren't available data for the requested values."),
                    Utils.chat_message("Do you want to filter on other metadata?"),Utils.choice('Available metadatum', self.available_keys, show_help=True,
                                     helpIconContent=messages.fields_help)], None, {}
