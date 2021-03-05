import itertools

class Utils(object):
    def chat_message(message: str):
        payload = {"sender": "bot",
                   "text": message}
        return {"type" : "message", "payload" : payload}

    def choice(caption, list_params, show_search=False, show_details=False, show_help=False, helpIconContent=''):
        elements = []
        if show_search and show_details and show_help:
            raise Exception('Not implemented yet')
        elif show_search and show_details and not show_help:
            raise Exception('Not implemented yet')
        elif show_search and not show_details and show_help:
            for i in list_params:
                elements.append({'name': i, 'value': list_params[i]})
            return {"type": "available_choices",
                    "payload": {
                        "showSearchBar": show_search,
                        "showDetails": show_details,
                        "caption": caption,
                        "showHelpIcon": show_help,
                        "helpIconContent" : helpIconContent,
                        "elements": elements}}
        elif show_search and not show_details and not show_help:
            for i in list_params:
                elements.append({'name': i, 'value': list_params[i]})
        elif not show_search and show_details and show_help:
            raise Exception('Not implemented yet')
        elif not show_search and show_details and not show_help:
            raise Exception('Not implemented yet')
        elif not show_search and not show_details and show_help:
            for i in list_params:
                elements.append({'name': i, 'value': list_params[i]})
            return {"type": "available_choices",
                    "payload": {
                        "showSearchBar": show_search,
                        "showDetails": show_details,
                        "caption": caption,
                        "showHelpIcon": show_help,
                        "helpIconContent": helpIconContent,
                        "elements": elements}}
        else:
            for i in list_params:
                elements.append({'name': i, 'value': list_params[i]})

        return {"type": "available_choices",
                "payload": {
                    "showSearchBar": show_search,
                    "showDetails": show_details,
                    "caption": caption,
                    "showHelpIcon": show_help,
                    "elements": elements}}

    def param_list(param_dict):
        elements = []
        for i in param_dict:
            elements.append({'field': i, 'values': param_dict[i]})
        return {"type" : "parameters_list",
                "payload" : elements}

    def create_piecharts(context, gcm_filter):
        msgs = []
        msgs.append(Utils.tools_setup('dataviz','dataset'))
        values = {k:v for (k,v) in list(
            sorted(
                [(x, context.payload.database.retrieve_values(gcm_filter, x)) for x in context.payload.database.fields_names if x not in context.payload.status],
                key = lambda x : len(x[1])))[:6]}
        copy_val = values.copy()
        for k, v in copy_val.items():
            if len(v)<=1:
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
        return {"type" : "data_summary",
                "payload" : {
                    "viz":viz
                }}

    def hist(values, title):
        viz = [{"vizType": "histogram",
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
        df = df.T
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

    def scatter(x,y,labels, u_labels):
        dict_scat = []
        #for l in u_labels:
        #    for ax in x[labels==l]:
        #        for ay in y[labels==l]:
        #            dict_scat.append({'x': ax, 'y': ay, 'label': l})
        #for ax in x:
        #    for ay in y:
         #       for l in u_labels:
         #           dict_scat.append({'x':ax,'y':ay,'label':l})
        dict_scat1 = {}
        for l in u_labels:
            dict_scat1[l]={}
            dict_scat1[l]['x']=x[labels==l]
            dict_scat1[l]['y']=y[labels == l]

        dict_scat = list(itertools.chain(*[[{'label': str(l), 'x': float(vv[0]), 'y': float(vv[1])} for vv in v] for l, v in
                               [(k, list(zip(v['x'], v['y']))) for (k, v) in dict_scat1.items()]]))
        #dict_scat = [{"x": ax, "y": ay, "label": l} for l, d in dict_scat1.items() for ax in d['x'] for ay in d['y']]

        print(dict_scat)
        return {
            "type": "scatter",
            "data": dict_scat,
        }

    def pyconsole_debug(payload):
        print("################## DEBUG: {}".format(payload))
