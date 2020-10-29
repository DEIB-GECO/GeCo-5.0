import re
import statistics
from geco_conversation import *

class MetadataAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.metadata_help)]

    def on_enter(self):
        from .confirm import Confirm
        self.context.payload.update('fields', {'metadata': {}})
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'metadata']}

        keys = self.context.payload.database.find_all_keys(gcm_filter)
        self.context.payload.insert('available_keys', {x.replace('_', ' '): x for x in keys if keys[x] > 1})
        #list_param = {k: self.status['fields'][k] for k in self.status['fields'] if k != 'metadata'}
        if len(self.status['available_keys']) >= 1:
            self.context.add_bot_msgs([Utils.chat_message(messages.metadata_filter)])#, Utils.param_list(list_param)])
            return None, False
        else:
            self.context.payload.back = MetadataAction
            return Confirm(self.context), True

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        self.context.payload.back = MetadataAction

        if intent == 'affirm':
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name','metadata']}
            keys = self.context.payload.database.find_all_keys(gcm_filter)
            self.context.payload.insert('available_keys', {x.replace('_', ' '): x for x in keys if keys[x] > 1})
            list_param = {k: self.status['fields'][k] for k in self.status['fields'] if k != 'metadata'}

            if len(self.status['available_keys']) > 1:
                self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_choice),
                        Utils.choice('Available metadatum', self.status['available_keys'], show_search=True,show_help=True,
                                     helpIconContent=helpMessages.fields_help),
                        Utils.param_list(list_param)])
                return KeyAction(self.context), False
            elif len(self.status['available_keys']) == 1:
                values, number = self.context.payload.database.find_key_values(gcm_filter, self.status['available_keys'].keys[0])
                if number == False:
                    list_values = {x['value']: x['value'] for x in values}
                    self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_value),
                            Utils.choice('Available values', list_values, show_search=True,show_help=True,
                                         helpIconContent=helpMessages.fields_help),
                            Utils.param_list(list_param)])
                    return StringValueAction(self.context), False
                else:
                    self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_range),
                               Utils.param_list(list_param)])
                    return RangeValueAction(self.context), False
            else:
                return Confirm(self.context), True

        elif intent == 'deny':
            return Confirm(self.context), True

        else:
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k != 'name' and k != 'metadata'}
            meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}

            k = message.lower().strip()
            if k.replace('_', ' ') in self.status['available_keys']:
                self.context.payload.insert('key',k)
                meta = self.status['fields'].copy()
                meta['metadata'].update({self.status['key'][0]: []})
                self.context.payload.replace('fields', meta)
                values, number = self.context.payload.database.find_key_values(str(k), gcm_filter, meta_filter)
                self.context.payload.insert('available_values',[val['value'] for val in values])

                list_param_chosen = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
                list_param_chosen.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                                          self.status['fields']['metadata'] if
                                          self.status['fields']['metadata'][x] != []})

                if number == False:
                    list_param = {x: x for x in self.status['available_values']}

                    self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_value),
                                               Utils.choice('Available values', list_param, show_search=True,show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list(list_param_chosen)])
                    return StringValueAction(self.context), False
                else:
                    numeric_values = [int(i) for i in self.status['available_values'] if i != None]
                    minimum = min(numeric_values)
                    maximum = max(numeric_values)
                    average = statistics.mean(numeric_values)
                    list_param = {'min: {}'.format(minimum): minimum, 'max: {}'.format(maximum): maximum,
                                  'mean: {}'.format(average): average}

                    self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_range),
                                               Utils.hist(numeric_values, self.status['key'][0]),
                                               Utils.choice('Ranges', list_param, show_help=True,
                                                            helpIconContent=helpMessages.fields_help),
                                               Utils.param_list(self.status['fields'])])
                    return RangeValueAction(self.context), False


class KeyAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.metadata_key_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k != 'name' and k != 'metadata'}
        meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}

        k =  message.lower().strip()
        if k.replace('_', ' ') in self.status['available_keys']:
            self.context.payload.insert('key',k)
            meta = self.status['fields'].copy()
            meta['metadata'].update({self.status['key'][0]: []})
            self.context.payload.replace('fields',meta)
            values, number = self.context.payload.database.find_key_values(str(k), gcm_filter, meta_filter)
            self.context.payload.insert('available_values',[val['value'] for val in values])

            list_param_chosen = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
            list_param_chosen.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                               self.status['fields']['metadata'] if self.status['fields']['metadata'][x]!=[]})

            if number==False:
                list_param = {x: x for x in self.status['available_values']}

                self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_value),
                        Utils.choice('Available values', list_param, show_search=True,show_help=True, helpIconContent=helpMessages.fields_help),
                        Utils.param_list(list_param_chosen)])
                return StringValueAction(self.context), False
            else:
                numeric_values = [int(i) for i in self.status['available_values'] if i!=None]
                if len(numeric_values)>1:
                    minimum = min(numeric_values)
                    maximum = max(numeric_values)
                    average = statistics.mean(numeric_values)
                    list_param = {'min: {}'.format(minimum):minimum, 'max: {}'.format(maximum):maximum, 'mean: {}'.format(average):average}
                    self.context.add_bot_msgs([Utils.chat_message(messages.metadatum_range), Utils.hist(numeric_values, self.status['key'][0]),
                                               Utils.choice('Ranges', list_param, show_help=True, helpIconContent=helpMessages.fields_help), Utils.param_list(self.status['fields'])])
                    return RangeValueAction(self.context), False
                else:
                    self.context.add_bot_msgs([Utils.chat_message(messages.other_metadatum)])
                    self.context.payload.delete('key')
                    return None, False

        return None, False

class StringValueAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.metadata_string_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        values = message.lower().strip().split(';')
        not_present = []
        for v in values:
            v=v.strip()
            if v in self.status['available_values']:
                val = self.status['fields'].copy()
                val['metadata'][self.status['key'][0]].append(v)
                self.context.payload.replace('fields', val)
            else:
                not_present.append(v)
        if len(self.status['fields']['metadata'][self.status['key'][0]])==0:
            self.context.payload.delete('fields', self.status['fields']['metadata'][self.status['key'][0]])
            #del(self.status['fields']['metadata'][self.status['key']])
        #self.status['fields']['metadata'].update({self.status['selected_key']: self.status[self.status['selected_key']]})

        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x != 'metadata'}
        list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in
                       self.status['fields']['metadata']})

        if not_present==[]:
            self.context.add_bot_msgs([Utils.chat_message(messages.chosen_values),
                    Utils.chat_message(messages.other_metadata),
                    Utils.choice('Available metadatum', self.status['available_keys'], show_help=True,
                                 helpIconContent=helpMessages.fields_help),
                    Utils.param_list(list_param)])
            return MetadataAction(self.context), False
        else:
            if not_present==values:
                self.context.payload.delete(self.status['key'][0])
                #del(self.status[self.status['key']])
            self.context.add_bot_msgs([Utils.chat_message("You selected {}, not present in the choices.\nThe other choices are in the bottom right pane.".format(",".join(i for i in not_present))),
                    Utils.choice('Available metadatum', self.status['available_keys'], show_help=True,
                                 helpIconContent=helpMessages.fields_help),
                    Utils.chat_message(messages.other_metadata)])
            return MetadataAction(self.context), False

class RangeValueAction(AbstractAction):

    def help_message(self):
        return [Utils.chat_message(helpMessages.metadata_range_help)]

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        value_low = -99999999999999999999999999999999999999999999999999999
        value_high = 99999999999999999999999999999999999999999999999999999
        v = message.lower().strip()
        high = ['lower than', 'lower', 'smaller than', 'smaller', 'max is', 'max', 'maximum is', 'maximum', 'less than', 'less']
        low = ['higher than', 'higher', 'bigger than', 'bigger', 'min is', 'min', 'minimum is', 'minimum', 'more than', 'more']
        for l in high:
            if l in v:
                res = re.search(r'{0}\s*(\d+)'.format(re.escape(l)), message)
                print(res.groups())
                print(res.group(0))
                print(res.group(1))
                value_high = int(res.group(1))
                break

        for h in low:
            if h in v:
                res = re.search(r'{0}\s*(\d+)'.format(re.escape(h)), message)
                print(res)
                print(res.groups())
                print(res.group(0))
                print(res.group(1))
                value_low = int(res.group(1))
                break
        numeric_values = [int(i) for i in self.status['available_values'] if i!=None]
        for v in numeric_values:
            if (v>value_low) and (v<value_high):
                val = self.status['fields'].copy()
                val['metadata'][self.status['key'][0]].append(v)
                self.context.payload.replace('fields', val)
                #self.status['fields']['metadata'][self.status['key']].append(v)

        list_param = {x: self.status['fields'][x] for x in self.status['fields'] if x!='metadata'}
        list_param.update({'metadata': '{}: {}'.format(x, self.status['fields']['metadata'][x]) for x in self.status['fields']['metadata']})

        if len(self.status['fields']['metadata'][self.status['key'][0]])>0:
            self.context.add_bot_msgs([Utils.chat_message("Ok!"),Utils.chat_message(messages.other_metadata),
                    Utils.choice('Available metadatum', self.status['available_keys'], show_search=True,show_help=True,
                                 helpIconContent=helpMessages.fields_help),
                    Utils.param_list(list_param), Utils.hist(numeric_values, self.status['key'][0])])
            return MetadataAction(self.context), False
        else:
            self.context.add_bot_msgs([Utils.chat_message(messages.no_metadata_range),
                                       Utils.chat_message(messages.other_metadata), Utils.choice('Available metadatum', self.status['available_keys'], show_search=True,show_help=True,
                                                                                                                    helpIconContent=helpMessages.fields_help)])
            return MetadataAction(self.context), False
