import json
with open('project_meta.json','r') as f:
    state = json.load(f)
    print(f.name.split('.',1)[0])
    f.close()

with open('./geco_conversation/'+f.name.split('.',1)[0].lower()+'.py', 'w') as f:
    f.write('from geco_conversation import *')
    for i in state.keys():
        f.write('\n')
        f.write('class '+ str(i)+'(AbstractAction):')
        f.write('\n')
        f.write('\tdef  help_message(self):\n')
        if 'help' in state[i]:
            msg_help = state[i]['help']
            if isinstance(msg_help, list):
                msgs = ['Utils.chat_message(' + x + ')' for x in msg_help]
                f.write('\t\tself.context.add_bot_msgs(' + str(msgs) + ')\n')
            elif isinstance(msg_help, str):
                msg = 'Utils.chat_message(' + msg_help + ')'
                f.write('\t\tself.context.add_bot_msg("' + msg + '")\n')
        else:
            f.write('\t\tpass')
        f.write('\n')
        f.write('\tdef on_enter(self):\n')
        if 'on_enter' in state[i]:
            msg_on_enter= state[i]['on_enter']
            if isinstance(msg_on_enter, list):
                msgs = ['Utils.chat_message('+x+')' for x in msg_on_enter]
                f.write('\t\tself.context.add_bot_msgs(' + str(msgs) + ')\n')
            elif isinstance(msg_on_enter, str):
                msg = 'Utils.chat_message('+msg_on_enter+')'
                f.write('\t\tself.context.add_bot_msg("'+msg+'")\n')
        else:
            f.write('\t\tpass')
        f.write('\n')
        f.write('\tdef logic(self,message, intent, entities):\n')
        for k in state[i].keys():
            if k not in ['on_enter', 'next', 'bool']:
                f.write('\t\t' + k+':')
                f.write('\n')
                for j in state[i][k].keys():
                    if j=='message':
                        msg = state[i][k]["message"]
                        if isinstance(msg, list):
                            f.write('\t\t\tself.context.add_bot_msgs(' + str(msg) + ')\n')
                        elif isinstance(msg_on_enter, str):
                            f.write('\t\t\tself.context.add_bot_msg("' + msg + '")\n')
                    elif j=='next':
                        next_state = state[i][k]['next']
                        bool = state[i][k]['bool']
                        f.write('\t\t\treturn ' + next_state + ', ' + str(bool) + '\n')
                    elif j=='bool':
                        pass
                    # else:
                    #     f.write('\t\t\t' + k + ':')
                    #     f.write('\n')
                    #     for q in state[i][k][j].keys():
                    #         if q == 'message':
                    #             msg = state[i][k][j]["message"]
                    #             if isinstance(msg, list):
                    #                 f.write('\t\t\t\tself.context.add_bot_msgs(' + str(msg) + ')\n')
                    #             elif isinstance(msg_on_enter, str):
                    #                 f.write('\t\t\t\tself.context.add_bot_msg("' + msg + '")\n')
                    #         elif q == 'next':
                    #             next_state = state[i][k][j]['next']
                    #             f.write('\t\t\treturn ' + next_state + ', ' + str(bool) + '\n')
                    #             bool = state[i][k][j]['bool']
                    #             f.write('\t\t\treturn ' + next_state + ', ' + str(bool) + '\n')
                    #         elif q == 'bool':
                    #             pass
                    #         else:
                    #             f.write('\t\t\t' + k + ':')
                    #             f.write('\n')
                    # f.write('\n')
        if 'next' in state[i]:
            next_state = state[i]['next']
            bool = state[i]['bool']
            f.write('\t\treturn '+next_state+', '+str(bool)+'\n')
    f.close()
'''
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
    '''