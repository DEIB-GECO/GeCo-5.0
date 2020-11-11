state = {}
state['JoinPivotAction'] = {}
state['JoinPivotAction']['on_enter'] = 'Can you tell me the joinby value?'
state['JoinPivotAction']['if(intent)=="yes"'] = {'message': 'Ok, I will do the joinby.', 'next':'PivotAction(self.context)', 'bool':True}
import json
with open('pipeline.json','r') as f:
    state = json.load(f)
    f.close()

for i in state.keys():
    with open('./geco_conversation/'+i.lower()+'.py', 'w') as f:
        f.write('from geco_conversation import *')
        f.write('\n')
        f.write('class '+ str(i)+'(AbstractAction):')
        f.write('\n')
        f.write('\tdef on_enter(self):\n')
        msg_on_enter= state[i]['on_enter']
        if isinstance(msg_on_enter, list):
            f.write('\t\tself.context.add_bot_msgs(' + str(msg_on_enter) + ')\n')
        elif isinstance(msg_on_enter, str):
            f.write('\t\tself.context.add_bot_msg("'+msg_on_enter+'")\n')
        else:
            f.write('\t\tpass')
        f.write('\n')
        f.write('\tdef logic(self,message, intent, entities):\n')
        for k in state[i].keys():
            if k not in ['on_enter', 'next', 'bool']:
                f.write('\t\t' + k+':')
                f.write('\n')
                msg = state[i][k]["message"]
                if isinstance(msg, list):
                    f.write('\t\t\tself.context.add_bot_msgs(' + str(msg) + ')\n')
                elif isinstance(msg_on_enter, str):
                    f.write('\t\t\tself.context.add_bot_msg("' + msg + '")\n')
                if next in state[i][k]:
                    next_state = state[i][k]['next']
                    bool = state[i][k]['bool']
                f.write('\n')
        next_state = state[i]['next']
        bool = state[i]['bool']
        f.write('\t\treturn '+next_state+', '+str(bool))
        f.close()