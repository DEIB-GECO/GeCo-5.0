from data_structure.database import *


class Utils(object):
    def chat_message(message: str):
        payload = {"sender": "bot",
                   "text": message}
        return {"type" : "message", "payload" : payload}

    def choice(caption, list_params, show_search=False, show_details=False, show_help=False, helpIconContent=''):
        elements = []
        #print(list_params)
        count=0
        for i in list_params:
            if(i== 'is_healthy'):
                elements.append({'name': 'Health', 'value': 'Health' })
                count=count+1
            else:
                if(type(i) == str):
                    b=i.replace('_',' ')
                    elements.append({'name': b, 'value': list_params[i]})
                    #print(i)
                else:

                    elements.append({'name': i, 'value': list_params[i]})
                count=count+1
            if(count>=15):
                show_search=True

        return {"type": "available_choices",
                "payload": {
                    "showSearchBar": show_search,
                    "showDetails": show_details,
                    "caption": caption,
                    "showHelpIcon": show_help,
                    "elements": elements}}

    def param_list(param_dict):
        elements = []
        #print(param_dict)

        if (param_dict==None):
            return {"type": "",
                    "payload": ""}

        for i in param_dict:
            #print(i)
            elements.append({'field': i, 'values': param_dict[i]})

        return {"type" : "parameters_list",
                "payload" : elements}

    def create_piecharts(db, gcm_filter,parameter_list):
        msgs = []
        #print("utils:",parameter_list)
        #print("gcm_filter:",gcm_filter)
        #print("db.fields_name",db.fields_names)
        msgs.append(Utils.tools_setup('dataviz','dataset'))


        values = {k:v for (k,v) in list(sorted(
                [(x, db.retrieve_values(gcm_filter, x)) for x in db.fields_names if x not in parameter_list ], #and x!='is_healthy'# and x.lower()!='health'],
                key = lambda x : len(x[1])))[:6]}


        print("---------------------------------------------")
        #[(x, context.payload.database.retrieve_values(gcm_filter, x)) for x in context.payload.database.fields_names if x not in context.payload.status and x!='is_healthy'],
        #print(values)
        copy_val = values.copy()
        for k, v in copy_val.items():
            if len(v)==1:
                del(values[k])
        del(copy_val)

        msgs.append(Utils.pie_chart(values))
        return msgs


    def pie_chart(pie_dict):
        viz = []
        for (k,v) in pie_dict.items():
            viz.append({
                "vizType": "pie-chart",
                "title": k,
                "data": v
            })
           # print(viz)
        return {"type" : "data_summary",
                "payload" : {
                    "viz":viz
                }}

    def hist(values, title):
        viz = [{"vizType": "histDistChart",
                "title" : title,
            "data": values}]

        return {"type": "data_summary",
                "payload": {
                    "viz": viz
                }}

    def tools_setup(add, remove):
        return {"type" : "tools_setup",
                "payload": {
                    "add" : [add],
                    "remove" : [remove]}}

    def workflow(state, download=False, link_list=[]):
        if download:
            return {"type": "workflow",
                    "payload": {"state": state,
                                "url": link_list}}
        else:
            return {"type": "workflow",
                    "payload": {"state": state}}

    def table_viz(show, df, show_index=True, order_by=None):
        data = df.to_dict()
        return {"type": "table",
                    "show": show,
                    "payload": {
                            "data":data,
                        "options":{
                                "show_index": show_index
                                #"order_by": string
                        }
                }}



    def pyconsole_debug(payload):
        print("################## DEBUG: {}".format(payload))
