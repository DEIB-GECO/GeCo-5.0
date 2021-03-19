import re
import statistics
from geco_conversation import *
from data_structure.operations import LogicalOperation


class RegionAction(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.region_help)])
        return None, True


    def on_enter(self):
        from .confirm import Confirm
        self.context.payload.back = RegionAction
        self.context.payload.insert('region', {})
        if 'fields' in self.status:
            gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'metadata']}
        else:
            gcm_filter={}
        if 'fields' in self.status and 'metadata' in self.status['fields']:
            meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}
            regions = self.db.find_regions(gcm_filter, meta_filter)
        else:
            regions = self.db.find_regions(gcm_filter, {})
        print(regions)
        if regions!= None:
            self.context.payload.insert('available_regions', {x: x for x in regions})
        else:
            self.context.payload.insert('available_regions',None)
        return Confirm(self.context), True


# def on_enter(self):
#     from .confirm import Confirm
#     self.context.payload.back = RegionAction
#     self.context.payload.insert('region', {})
#     gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'metadata']}
#     if 'metadata' in self.status['fields']:
#         meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}
#         regions = self.context.payload.database.find_regions(gcm_filter,meta_filter)
#     else:
#         regions = self.context.payload.database.find_regions(gcm_filter,{})
#     self.context.payload.insert('available_regions', {x: x for x in regions})
#     #list_param = {k: self.status['fields'][k] for k in self.status['fields'] if k != 'metadata'}
#     self.context.add_bot_msgs([Utils.chat_message(messages.region_filter)])#, Utils.param_list(list_param)])
#     return None, False

    def logic(self, message, intent, entities):
        from .confirm import Confirm
        self.context.payload.back = RegionAction

        if intent == 'affirm':
            list_param = {k: self.status['fields'][k] for k in self.status['fields'] if k not in 'metadata'}
            if 'metadata' in self.status['fields']:
                list_param.update({k: self.status['metadata'][k] for k in self.status['fields']['metadata']})

            self.context.add_bot_msgs([Utils.chat_message(messages.region_choice),
                                       Utils.choice('Available regions', self.status['available_regions'], show_search=True,
                                                    show_help=True,
                                                    helpIconContent=helpMessages.fields_help),
                                       Utils.param_list(list_param)])
            return RegionAction2(self.context), False
        elif intent == 'deny':
            return Confirm(self.context), True


class RegionAction2(AbstractDBAction):

    def help_message(self):
        self.context.add_bot_msgs([Utils.chat_message(helpMessages.region_key_help)])
        return None, False

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        gcm_filter = {k: v for (k, v) in self.status['fields'].items() if k not in ['name', 'metadata']}
        region_filter = {k: v for (k, v) in self.status['regions'].items()}
        if 'metadata' in self.status['fields']:
            meta_filter = {k: v for (k, v) in self.status['fields']['metadata'].items()}

        k = message.lower().strip()
        if (k in self.status['available_regions']):
            self.context.payload.insert('reg', k)
            region = self.status['regions'].copy()
            region.update({self.status['reg'][0]: []})
            self.context.payload.replace('regions', region)
            self.context.add_bot_msgs([Utils.chat_message('Sorry, not implemented yet')])
            return RegionAction(self.context), False
        else:
            self.context.add_bot_msgs([Utils.chat_message('Sorry, I don\'t understand')])
            return RegionAction2(self.context), False
