
class Utils(object):
    def chat_message(message):
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

    def hist(values):
        viz = {"vizType": "hist_dist_chart",
            "data": values}

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
                                "url": link_list[0]}}
        else:
            return {"type": "workflow",
                    "payload": {"state": state}}


    def pyconsole_debug(payload):
        print("################## DEBUG: {}".format(payload))
