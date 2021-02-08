from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import (
    UserUtteranceReverted,
    ActionReverted,

)

from database_rasa import *
from dataset import DataSet
from workflow.workflow_class import Workflow
from workflow.clustering import KMeans
from workflow.gmql import Select
from utils import *
import pandas as pd

#import rasa.core.channels.socketio as file

Selection_list = []
old_value = ""
data = experiment_fields
ann = False
#database1 = DB(experiment_fields,False,[1,2])
predefNameDb= "DS_" 
number = 0
workflow = Workflow()
show=[]
last =1
param_list={}
metadatum_list={}
R=0

#Utils.pie_chart({'Annotations': 'annotations', 'Experimental data': 'experiments'})


#Slots = {'source': 1, 'data_type': 2, 'assembly': 3,
 #        'file_format': 4, 'biosample_type': 5, 'tissue': 6, 'cell': 7,
 #        'disease': 8,
 #        'technique': 9, 'feature': 10, 'target': 11}


#print(Slots['source'])

all_db = database()
db= DB(data,ann,all_db)
self = []

#c= database.find_all_keys(self)
#print(c.metadata)

#all_val=all_db.values
#dbfields= db.values

#c=db.find_all_keys1({"key" :["age"]})
#print(c)
#c=db.find_all_keys({"%a%":["%a%"]})
#print(c)

#c=database.get_all_values

#print(all_val)
#print(dbfields)

meta_list={}
saved_metadatum_msg  = []
saved_metadatum_value = []


###############################
###   Variabili k-kluster   ###
###############################

Min_Max_cluster = int
N_cluster = int
Min_cluster = int
Max_cluster = int

###############################
### Per testare sulla shell ###
###############################
shell = False

#################################################################################################
#######################################  SELECT  ################################################
#################################################################################################
class WhatData(Action):

    def name(self) -> Text:
        return "action_what_data"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        d = {'Annotations': 'annotations', 'Experimental data': 'experiments'}

        list_param = {x: x for x in db.fields_names}

        if(shell == False):
            dispatcher.utter_message(Utils.choice("Data available", d))
            dispatcher.utter_message(Utils.workflow("Data Selection"))

            msg = Utils.create_piecharts(db,{"field":"source"} , [])
            for m in msg:
                dispatcher.utter_message(m)

            dispatcher.utter_message(Utils.create_piecharts(db,list_param,param_list))

        else:
            print("Data available {}".format(d))

        return []

class MoreFields(Action):

    def name(self) -> Text:
        return "action_give_exact_experiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global db, data, ann, old_value,experiment_fields,param_list,Selection_list

        data2 = tracker.get_slot("annotations")
        if (data2 != None):
            data= annotation_fields
            ann= True
            db = DB(data, ann,all_db)

        else:
            db = DB(experiment_fields,False,all_db)

        print ('sono in more fiedls')

        field= tracker.get_slot('field')
        source = tracker.get_slot("source")
        data_type = tracker.get_slot("data_type")
        assembly = tracker.get_slot("assembly")
        file_format = tracker.get_slot("file_format")
        biosample_type = tracker.get_slot("biosample_type")
        tissue = tracker.get_slot("tissue")
        cell = tracker.get_slot("cell")
        disease = tracker.get_slot("disease")
        technique = tracker.get_slot("technique")
        feature = tracker.get_slot("feature")
        target = tracker.get_slot("target")

        dict_selection = {}

        if(param_list == {} or param_list == None):
            if(ann == False):
                param_list = {"Data":"Experiments"}
            else:
                param_list = {"Data":"Annotations"}

        Slots= {'source':source , 'data_type':data_type,'assembly':assembly,
                'file_format':file_format,'biosample_type':biosample_type,'tissue':tissue,'cell':cell,'disease':disease,
                'technique':technique,'feature':feature,'target':target}

        if (field != None):
            print(field, "sono un chatbot scemo")

            print('sono in exact experiments')
            request_field = tracker.get_slot("field")
            print('request_field:', request_field)
            request_field_db = request_field + '_db'
            request_value = tracker.get_slot(request_field)

            # field_db = getattr(database, request_field_db)
            list_param = {x: x for x in db.fields_names}

            if (request_field == None):
                dispatcher.utter_message("nessun campo selezionato")

            elif ((request_field != "is_healthy")):  #(request_value != old_value) and
                # if (request_field not in domain['slots']['field']['values']) or (request_field not in db.fields_names):
                if ((request_value not in domain['slots'][request_field]['values']) or (
                        request_field not in db.fields_names) or (request_value not in db.values[request_field])):
                    dispatcher.utter_message("The chosen value (exact experiment) is not correct. Choose between:")
                    # dispatcher.utter_message("The possible values for {} are: {}".format(request_field,field_db))

                else:
                    for x in db.values[request_field]:
                        if (x != None):
                            print(x)
                            if (request_value in x):
                                c = x
                                print('eureka', c)

                    #dispatcher.utter_message("Succesful choice")
                    Selection_list.append([request_field, request_value])
                    print(Selection_list)
                    old_value = request_value
                    dict_selection = {}

                    for num, name in enumerate(Selection_list):
                        if (name[1] == False):
                            dict_selection.update({name[0]: ['false']})

                        elif (name[1] == True):
                            dict_selection.update({name[0]: ['true']})

                        else:
                            dict_selection.update({name[0]: [name[1]]})

                    if (dict_selection != {}):
                        param_list.update(dict_selection)

                    db.update(dict_selection)
                    if (shell == False):
                        dispatcher.utter_message(Utils.param_list(param_list))


            else:
                dispatcher.utter_message("The chosen value (else) is not correct. Choose between:")
                dispatcher.utter_message("{}".format(db.fields_names))

            return []

       # for name1 in Slots_2:
       #     if (name1!= None):
       #         print('name1',name1)
        for num, name  in enumerate(Slots):
            print('name',Slots[name])
            if (Slots[name] != None):
                    #if(name1 == name):
                #dispatcher.utter_message("Succesful choice")
                Selection_list.append([name,Slots[name]])
                print(Selection_list)

        for num, name in  enumerate(Selection_list):
            if(name[1] == False):
                dict_selection.update({name[0] : ['false']})

            elif(name[1] == True):
                dict_selection.update({name[0] : ['true']})

            else:
                dict_selection.update({name[0] : [name[1]]})


        if (dict_selection != {}):
            param_list.update(dict_selection)

        db.update(dict_selection)
        return []

class GiveExactExperiment(Action):

    def name(self) -> Text:
        return "action_give_exact_experiment_old"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global db, data, ann, old_value, param_list

        data2 = tracker.get_slot("annotations")
        if (data2 != None):
            data= annotation_fields
            ann= True
            db = DB(data, ann, all_db )

        print ('sono in exact experiments')
        request_field = tracker.get_slot("field")
        print('request_field:',request_field)
        request_field_db = request_field + '_db' 
        request_value = tracker.get_slot(request_field)

       # field_db = getattr(database, request_field_db)
        list_param = {x: x for x in db.fields_names}

        if(request_field == None):
            dispatcher.utter_message("nessun campo selezionato")

        elif((request_field != "is_healthy")): #(request_value != old_value) and
            #if (request_field not in domain['slots']['field']['values']) or (request_field not in db.fields_names):
            if ((request_value not in domain['slots'][request_field]['values']) or (
                    request_field not in db.fields_names) or (request_value not in db.values[request_field])):
                dispatcher.utter_message("The chosen value (exact experiment) is not correct. Choose between:")
                #dispatcher.utter_message("The possible values for {} are: {}".format(request_field,field_db))

            else:
                for x in db.values[request_field]:
                    if(x!= None):
                        print(x)
                        if(request_value in x):
                            c=x
                            print('eureka',c)

                #dispatcher.utter_message("Succesful choice")
                Selection_list.append([request_field,request_value])
                print(Selection_list)
                old_value=request_value
                dict_selection= {}

                for num, name in  enumerate(Selection_list):
                    if(name[1] == False):
                        dict_selection.update({name[0] : ['false']})

                    elif(name[1] == True):
                        dict_selection.update({name[0] : ['true']})

                    else:
                        dict_selection.update({name[0] : [name[1]]})

                if(dict_selection != {}):
                    param_list.update(dict_selection)

                db.update(dict_selection)
                if(shell == False):
                    dispatcher.utter_message(Utils.param_list(param_list))


        else:
            dispatcher.utter_message("The chosen value (else) is not correct. Choose between:")
            dispatcher.utter_message("{}".format(db.fields_names))

        return []

class SelectData(Action):

    def name(self) -> Text:
        return "action_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global database, data, ann, all_db,db

        data1 = tracker.get_slot("experiments")
        data2 = tracker.get_slot("annotations")

        if(data1 != None and ann != False):           
            data = experiment_fields
            ann = False
            db = DB(data, ann, all_db)

        elif(data2 != None):
            print("annotation")
            data= annotation_fields 
            ann= True
            db = DB(data, ann, all_db)

        else:
            print("experiments")
            return []

        return [SlotSet("field", None),SlotSet("is_healthy", None), SlotSet("cell", None),SlotSet("source", None),SlotSet("tissue", None),SlotSet("file_format", None),SlotSet("assembly", None),SlotSet("feature", None),SlotSet("disease", None),SlotSet("data_type", None),SlotSet("content_type", None),SlotSet("technique", None),SlotSet("target", None),SlotSet("experiments", None),SlotSet("annotations", None)]

class ShowField(Action):

    def name(self) -> Text:
        return "action_show_field"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global ann, param_list

        list_param = {x: x for x in db.fields_names}

        if(param_list == {} or param_list == None):
            if(ann == False):
                param_list = {"Data":"Experiments"}
            else:
                param_list = {"Data":"Annotations"}

        if(shell == False):
            msg = Utils.create_piecharts(db, {}, [])
            for m in msg:
                dispatcher.utter_message(m)
            dispatcher.utter_message(Utils.choice("Available Fields", list_param,show_help=True))
            dispatcher.utter_message(Utils.param_list(param_list))
            dispatcher.utter_message(Utils.create_piecharts(db,list_param,param_list))

        else:
            print ("Available Fields", list_param)

        return []

class ShowValue(Action):

    def name(self) -> Text:
        return "action_show_value"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        request_field = tracker.get_slot("field")
        request_field_db = request_field + '_db'        

        for num, name in  enumerate(Selection_list):
            if(request_field == name[0]):
                dispatcher.utter_message("Insert field or modify field?")
                d = {'Insert': 'Insert', 'Modify': 'Modify'}
                if (shell == False):
                    dispatcher.utter_message(Utils.choice("Options", d ))
                else:
                    print("Options {}".format(d))

                return []
        print('req_field',request_field)
       # for x in domain['slots']['field']['values']:
       #     print('x',x)
       # for y in   db.fields_names:
       #     print('y',y)
        if (request_field not in domain['slots']['field']['values']) or (request_field not in db.fields_names):
            dispatcher.utter_message("The chosen value (tracker get out) is not correct. Choose between:")
            if(shell == False):
                dispatcher.utter_message("{}".format(db.fields_names))
            else:
                print("{}".format(db.fields_names))

            return[]

        else:
            list_param = {x: x for x in db.values[request_field]}
           # print("lista", db.values[request_field])

           # dispatcher.utter_message("The possible values for {} are:".format(request_field))
            if(shell == False):
               # values = {k: v for (k, v) in list(
                #    sorted(
                 #       [(x, db.retrieve_values({}, x)) for x in db.fields_names if x in list_param ],
                  #      key=lambda x: len(x[1])))[:6]}
                #print(values)

                msg = Utils.create_piecharts(db, list_param, [])
                for m in msg:
                    dispatcher.utter_message(m)
                dispatcher.utter_message(Utils.choice("Fields", list_param, show_help=True,))
            else:
                print("Fields", list_param)

        return []

class CheckValue(Action):

    def name(self) -> Text:
        return "action_check_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print ('sono in checkValue')
        global old_value, param_list
        request_field = tracker.get_slot("field")

        if(request_field == None):
            dispatcher.utter_message("nessun campo selezionato")

        else:
            request_field_db = request_field + '_db'
            request_value = tracker.get_slot(request_field)
        
            if( (request_field != "is_healthy")): #(request_value != old_value) and
                #print('req_field',request_field)
                #for x in db.fields_names:
                #    print('x', x)
                #for y in db.values[request_field]:
                #    print('y', y)
                #print('req_value',request_value)
                #if(request_field not in db.fields_names):
                #    print('aloa')
                #if(request_value not in db.values[request_field]):
                #    print('cracatoa')
                if ((request_field not in db.fields_names) or (request_value not in db.values[request_field])):
                #if ((request_value not in domain['slots'][request_field]['values']) or (
                            #request_field not in db.fields_names) or (request_value not in db.values[request_field])):

                    dispatcher.utter_message("The chosen value (!= 435 !) was not correct.")
                    #dispatcher.utter_message("The possible values for {} are: {}".format(request_field,field_db))

                else: 
                    #dispatcher.utter_message("Succesful choice")
                    Selection_list.append([request_field,request_value])
                    print(Selection_list)
                    old_value=request_value
                    dict_selection= {}

                    for num, name in  enumerate(Selection_list):
                        if(name[1] == False):
                            dict_selection.update({name[0] : ['False']})

                        elif(name[1] == True):
                            dict_selection.update({name[0] : ['True']})

                        else:
                            dict_selection.update({name[0] : [name[1]]})

                    db.update(dict_selection)
                    if(dict_selection != {}):
                        param_list.update(dict_selection)

                    #z=db.find_all_keys(dict_selection)
                    #print("al keys é:", z)
                    if(shell == False):
                        dispatcher.utter_message(Utils.param_list(param_list))
                    else:
                        print(param_list)
                    return [SlotSet("field", None)]


            elif(request_value in Selection_list):
                dispatcher.utter_message("ok")

            else:
                dispatcher.utter_message("The chosen value (else) is not correct. Choose between:")
                dispatcher.utter_message("{}".format(db.fields_names))

        return []

class YesNo(Action):

    def name(self) -> Text:
        return "action_yes_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_param = {'Yes': 'Yes', 'No': 'No'}

        if (shell == False):
            dispatcher.utter_message(Utils.choice("Data Types", list_param))
        else:
            dispatcher.utter_message("Options {}".format(list_param))

        return []

class HealthYes(Action):

    def name(self) -> Text:
        return "action_is_healthy_yes"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                   
        if(ann == True):
            dispatcher.utter_message("The chosen value (healthyes) is not correct. Choose between:")
            dispatcher.utter_message("{}".format(db.fields_names))
            return[]

        else:
            for num, name in  enumerate(Selection_list):
                if(name == ['is_healthy',False]):
                    del Selection_list[num]

                elif(name == ['is_healthy',True]):
                    del Selection_list[num]

                else:
                    pass      
        
            Selection_list.append(["is_healthy",True])
            dict_selection= {}
            for num, name in  enumerate(Selection_list):
                if(name[1] == False):
                    dict_selection.update({name[0] : ['False']})

                elif(name[1] == True):
                    dict_selection.update({name[0] : ['True']})

                else:
                    dict_selection.update({name[0] : [name[1]]})

            db.update(dict_selection)
            if (dict_selection != {}):
                param_list.update(dict_selection)

            #z = db.find_all_keys(param_list)
            #print("al keys é:", z)

            if(shell == False):
                dispatcher.utter_message(Utils.param_list(param_list))

            return [SlotSet("is_healthy", 'yes')]

class HealthNo(Action):

    def name(self) -> Text:
        return "action_is_healthy_no"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if(ann == True):
            dispatcher.utter_message("The chosen value (healthno) is not correct. Choose between:")
            c = []
            for key in request_field:
                c.append(key)

            if (shell == False):
                dispatcher.utter_message(Utils.choice("Fields", c))
            else:
                dispatcher.utter_message("Options {}".format(c))

            return[]

        else:
            for num, name in  enumerate(Selection_list):
                if(name == ['is_healthy',True]):
                    del Selection_list[num]

                elif(name == ['is_healthy',False]):
                    del Selection_list[num]

                else:
                    pass
                
            Selection_list.append(["is_healthy",False])
            dict_selection= {}
            for num, name in  enumerate(Selection_list):
                if(name[1] == False):
                    dict_selection.update({name[0] : ['False']})

                elif(name[1] == True):
                    dict_selection.update({name[0] : ['True']})

                else:
                    dict_selection.update({name[0] : [name[1]]})

            db.update(dict_selection)

            if (dict_selection != {}):
                param_list.update(dict_selection)

            #z = db.find_all_keys(param_list)
            #         print("al keys é:", z)
            if(shell==False):
                dispatcher.utter_message(Utils.param_list(param_list))

            return [SlotSet("is_healthy", 'no')]

class Insert(Action):

    def name(self) -> Text:
        return "action_insert"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        request_field = tracker.get_slot("field")
        request_field_db = request_field + '_db'        
        #field_db = getattr(db, request_field_db)

        list_param = {x: x for x in db.values[request_field]}

        #c = []
        #list_param = {x: x for x in field_db}

        dispatcher.utter_message("The possible values for {} are:".format(request_field))
        if (shell == False):
            dispatcher.utter_message(Utils.choice("Fields", list_param))
        else:
            dispatcher.utter_message("Options {}".format(list_param))

        return []

class Modify(Action):

    def name(self) -> Text:
        return "action_modify"  

    def delete(self, request_field):
        for num,name in enumerate(Selection_list):
                if(name[0] == request_field):
                    del Selection_list[num]
                    print("campo cancellato")
                    self.delete( request_field)
        return []

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global db, data, ann

        request_field = tracker.get_slot("field")
        request_field_db = request_field + '_db'  

        db = DB(data, ann, all_db)
        self.delete(request_field)
        dict_selection= {}

        for num, name in enumerate(Selection_list):
            if(name[1] == False):
                dict_selection.update({name[0] : ['false']})

            elif(name[1] == True):
                dict_selection.update({name[0] : ['true']})

            else:
                dict_selection.update({name[0] : [name[1]]})

        print(dict_selection)

        db.update(dict_selection)

        list_param = {x: x for x in db.values[request_field]}

        dispatcher.utter_message("The possible values for {} are:".format(request_field))
        if (shell == False):
            dispatcher.utter_message(Utils.choice("Fields", list_param, show_help=True, ))
        else:
            dispatcher.utter_message("Options {}".format(list_param))

        return [SlotSet(request_field,None)]

class CheckSlots(Action):

    def name(self) -> Text:
        return "action_checkSlots"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cell =  tracker.get_slot("cell")
        source =  tracker.get_slot("source")
        tissue =  tracker.get_slot("tissue")
        file_format =  tracker.get_slot("file_format")
        assembly =  tracker.get_slot("assembly")
        feature =  tracker.get_slot("feature")
        disease =  tracker.get_slot("disease")
        data_type =  tracker.get_slot("data_type")
        content_type =  tracker.get_slot("content_type")
        target =  tracker.get_slot("target")
        technique =  tracker.get_slot("technique")
        is_healthy =  tracker.get_slot("is_healthy")
        dataset_name = tracker.get_slot('dataset_name')

        #field_db = getattr(database, request_field + '_db')
        global Selection_list

        if(dataset_name == None and ann==False):
            dispatcher.utter_message("Please select a dataset value")
            return[SlotSet("DS", False), SlotSet("field", "dataset_name")]


        return [SlotSet("DS", True)]

class Reset(Action):

    def name(self) -> Text:
        return "action_reset"          

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global Selection_list , db, ann, data, param_list,experiment_fields
        print("ho resettato")

        Selection_list = []
        param_list={}
        data = experiment_fields
        #ann = False
        #db = DB(data, ann, all_db)
       # meta_list = {}
        saved_metadatum_msg = []
        saved_metadatum_value = []
        R = 0

        if (shell == False):
            dispatcher.utter_message(Utils.param_list(param_list))

        return [SlotSet("DS", False),SlotSet("dataset_name", None),SlotSet("is_healthy", None), SlotSet("cell", None),SlotSet("source", None),SlotSet("tissue", None),SlotSet("file_format", None),SlotSet("assembly", None),SlotSet("feature", None),SlotSet("disease", None),SlotSet("data_type", None),SlotSet("content_type", None),SlotSet("technique", None),SlotSet("target", None),SlotSet("experiments", None),SlotSet("annotations", None)]

class ResetTotal(Action):

    def name(self) -> Text:
        return "action_reset_total"          

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global Selection_list , database, ann, data, workflow
        print("ho resettato tutto")

        Selection_list = []
        
        data = experiment_fields
        ann = False
        db = DB(data, ann, all_db)
        meta_list = {}
        saved_metadatum_msg = []
        saved_metadatum_value = []
        R = 0

        del workflow[-1]
                
        return [SlotSet("is_healthy", None), SlotSet("cell", None),SlotSet("source", None),SlotSet("tissue", None),SlotSet("file_format", None),SlotSet("assembly", None),SlotSet("feature", None),SlotSet("disease", None),SlotSet("data_type", None),SlotSet("content_type", None),SlotSet("technique", None),SlotSet("target", None),SlotSet("experiments", None),SlotSet("annotations", None)]

class RenameDatabase(Action):

    def name(self) -> Text:
        return "action_rename_database"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent=tracker.latest_message['intent'].get('name')
        message = tracker.latest_message.get('text')

        if( last_intent != "deny"):
            return [SlotSet("dataset_rename", message)]

        return[SlotSet("dataset_rename", None)]

class DownloadDatabase(Action):

    def name(self) -> Text:
        return "action_download_database"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global database, data, ann, number, predefNameDb, workflow, param_list

        message = tracker.get_slot("dataset_rename")
        if (message != None):
            db_name=message
        else:
            db_name = predefNameDb + str(number)
            number = number + 1
        dict_selection = {}
        for num, name in  enumerate(Selection_list):
            if(name[1] == False):
                dict_selection.update({name[0] : ['false']})

            elif(name[1] == True):
                dict_selection.update({name[0] : ['true']})

            else:
                dict_selection.update({name[0] : [name[1]]})

        #ds=DataSet(dict_selection, db_name) #invece di passare solo la dict_selection unisco anche il dizionario fatto dai metadati

        #workflow.add(Select(ds))

        #for num, name in  enumerate(workflow):
        #    c = num % 2

        param_list.update({"Name": db_name})

        #dispatcher.utter_message("OK, dataset saved with name: {}".format(db_name))

        if (shell == False):
            dispatcher.utter_message(Utils.param_list(param_list))

        #c=database.download(dict_selection)
        
        #with open(db_name + '.txt', 'w') as f:
        #    print('Filename:', c, file=f)

        return []

class ShowMetadatum(Action):

    def name(self) -> Text:
        return "action_show_metadatum"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global ann, param_list, database, Selection_list


        dict_selection = {}
        for num, name in enumerate(Selection_list):
            if (name[1] == False):
                dict_selection.update({name[0]: ['False']})

            elif (name[1] == True):
                dict_selection.update({name[0]: ['True']})

            else:
                dict_selection.update({name[0]: [name[1]]})

        z = db.find_all_keys(dict_selection)
        c={}
        for y in z:
            c.update({y:y})
            print(y)

        msg = Utils.create_piecharts(db, {}, [])
        for m in msg:
            m = ({'type': 'data_summary',
                  'payload': {'viz': [{'vizType': 'pie-chart', 'title': '', 'data': [{'value': '', 'count': 0}]}]}})
            dispatcher.utter_message(m)


        if(c != {} ):
            if(shell== False):

                dispatcher.utter_message(Utils.choice("First 50 metadatum:", c,show_search=True))
            else:
                dispatcher.utter_message("First 50 metadatum:")
                print(c)
        else:
            if (shell == False):
                dispatcher.utter_message(Utils.choice("Options:", {'Recap': 'Recap'}, show_search=True))
            else:
                dispatcher.utter_message("You can only recap no metadatum avaialble to filter")

        return []

class MetadatumType(Action):

    def name(self) -> Text:
        return "action_metadatum_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global saved_metadatum_msg, saved_metadatum_value,param_list,meta_list,Selection_list

        message = tracker.latest_message.get('text')
        saved_metadatum_msg=message

        param_list.update({saved_metadatum_msg:''})

        dict_selection = {}
        for num, name in enumerate(Selection_list):
            if (name[1] == False):
                dict_selection.update({name[0]: ['False']})

            elif (name[1] == True):
                dict_selection.update({name[0]: ['True']})

            else:
                dict_selection.update({name[0]: [name[1]]})

        if(shell==False):
            dispatcher.utter_message(Utils.param_list(param_list))

        z = db.find_key_values(message, dict_selection)
        print("z", z)
        c = {}
        # if(z[1] == False):
        for y in z[0]:
            print(y)
            #print(y['value'])
            c.update({y['value']: y['value']})
        # y[count] sono i valori che mi serviranno per l istogramma
        # print(y['count'])
        # c.update({y['count']: y['count']})

        if (z[1] == False):
            dispatcher.utter_message("Which value do you want select? if you want more separate with ;")

            if (shell == False):
                print("false",c)
                dispatcher.utter_message(Utils.choice('Available values', c, show_search=True, show_help=True))
                           #helpIconContent=helpMessages.fields_help)
            else:
                dispatcher.utter_message('Available values')
                print(c)

        elif(z[1] == True):
            dispatcher.utter_message("Which range of values do you want? You can tell me the minimum or maximum value or both.\n The values are shown in the histogram.")

            if (shell == False):
                print("true",c)
                dispatcher.utter_message(Utils.choice('Available values', c, show_search=True, show_help=True))

            else:
                dispatcher.utter_message('Available values')
                print(c)
        else:
            print('Errore')

            #Utils.choice('Ranges', MIX_MAX_MEAN, show_help=True, helpIconContent=helpMessages.fields_help)

        return []

class TakeValue(Action):

    def name(self) -> Text:
        return "action_take_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global saved_metadatum_msg, saved_metadatum_value, param_list, meta_list

        message = tracker.latest_message.get('text')

        print("ciao")

        if (';' not in message):
            print("ciao")
            saved_metadatum_value=message
           # print(saved_metadatum_msg)
            Meta = saved_metadatum_msg + ': ' + saved_metadatum_value
            meta_list.update( {saved_metadatum_msg: saved_metadatum_value } )
            param_list.update( {saved_metadatum_msg: saved_metadatum_value } )
            #print(meta_list)

            if(shell == False):
                dispatcher.utter_message(Utils.param_list(param_list))

        elif(';' in message):
            c= message.split(';')
            for i in c:
                print(c[i])

        return []


class SaveDb(Action):

    def name(self) -> Text:
        return "action_save_dataset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global param_list,workflow

        dict_selection = {}
        for num, name in enumerate(Selection_list):
            if (name[1] == False):
                dict_selection.update({name[0]: ['False']})

            elif (name[1] == True):
                dict_selection.update({name[0]: ['True']})

            else:
                dict_selection.update({name[0]: [name[1]]})

        print(param_list)
        print("name db:", param_list["Name"])

        ds=DataSet(dict_selection, param_list["Name"]) #invece di passare solo la dict_selection unisco anche il dizionario fatto dai metadati

        workflow.add(Select(ds))
        #for num, name in  enumerate(workflow):
        #   c = num % 2

#################################################################################################
######################################  Project    ##############################################
#################################################################################################


class KeepModify(Action):

    def name(self) -> Text:
        return "action_keep_modify"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        d = {'Keep my selection': 'I want to keep my selection', 'Modify the extracted selection': 'I want to modify the extracted data','Modify my selection':'I want to modify my selection'}

        if (shell == False):
            dispatcher.utter_message(Utils.choice("Options", d))

        return []


class GMQLBinaty(Action):

    def name(self) -> Text:
        return "action_GMQL_binary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        d = {'Join': 'Join', 'Union': 'Union','Map': 'Map', 'Difference': 'Difference'}

        if (shell == False):
            dispatcher.utter_message(Utils.choice("Options", d))

        return []

class Metadata(Action):

    def name(self) -> Text:
        return "action_metadata_exploration"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if(True == True):
            disaptcher.utter_message("Which value do you want to select?\n If you want more, please separate them using ';'.")

        else:
            dispatcher.utter_message("Which range of values do you want? You can tell me the minimum or maximum value or both.\n The values are shown in the histogram.")

        return []

class SetGMQL(Action):

    def name(self) -> Text:
        return "action_set_gmql"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        for num, name in  enumerate(workflow):
            c = num % 2

        if (c ==0 ):#number of dataset is odd new_dataset
            return [SlotSet("GMQL", True)]


        else: #number of dataset is even gmql_binary

            return [SlotSet("GMQL", False)]

class Join(Action):

    def name(self) -> Text:
        return "action_join"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("sei nel join")

        return []

class Union(Action):

    def name(self) -> Text:
        return "action_union"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("sei nel union")

        return []

class Map(Action):

    def name(self) -> Text:
        return "action_map"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message("sei nella map")

        return []

class Difference(Action):

    def name(self) -> Text:
        return "action_difference"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message("sei nella difference")

        return []

class Cover1(Action):

    def name(self) -> Text:
        return "action_cover_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return []

class Cover2(Action):

    def name(self) -> Text:
        return "action_cover_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []


class Cover3(Action):

    def name(self) -> Text:
        return "action_cover_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

class GmqlUnary(Action):

    def name(self) -> Text:
        return "action_GMQL_unary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if(shell== False):
            dispatcher.utter_message(Utils.choice('Unary_operations',{'Project metadata':'project metadata', 'Project region':'project region', 'Cover':'cover'}))

        return []

class Workflow(Action):

    def name(self) -> Text:
        return "action_workflow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent=tracker.latest_message['intent'].get('name')

        if (shell == False):

            if(last_intent == 'cluster'):
                dispatcher.utter_message(Utils.workflow("KMeans"))
                return []

            dispatcher.utter_message(Utils.choice('Options', {'Keep': 'keep',
                                                                       'Modify': 'modify'}))

            if(last_intent == 'project_metadata'):
                dispatcher.utter_message(Utils.workflow("Project Metadata"))


            elif(last_intent == 'project_region'):
                dispatcher.utter_message(Utils.workflow("Project Region"))




        return []

class ModifyKeep(Action):

    def name(self) -> Text:
        return "action_modify_keep"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent=tracker.latest_message['intent'].get('name')
        print(last_intent)

        if(last_intent == 'modify' ):

            dict_selection = {}
            for num, name in enumerate(Selection_list):
                if (name[1] == False):
                    dict_selection.update({name[0]: ['False']})

                elif (name[1] == True):
                    dict_selection.update({name[0]: ['True']})

                else:
                    dict_selection.update({name[0]: [name[1]]})

            z = db.find_all_keys(dict_selection)
            c = {}
            for y in z:
                c.update({y: y})
                print(y)

            ##---------------------------------------
            c = {}
            print(meta_list)
            for k, v in meta_list.items():
                print(k, v)
                print("messagio nella lista")
                print(meta_list)
                metadatum_exist = True
                c.update({k: k})
            ##--------------------------------------


            if (meta_list != {}):
                if (shell == False):
                    dispatcher.utter_message(Utils.choice("First 50 metadatum:", c, show_search=True))
                else:
                    dispatcher.utter_message("First 50 metadatum:")
                    print(c)

            return [SlotSet("modify_keep", 'modify')]


        elif (last_intent == 'keep'):
            return [SlotSet("modify_keep", 'keep')]
        else:
            print("ne keep ne modify")
            return[]


class ShowAllMetadatum(Action):

    def name(self) -> Text:
        return "action_show_all_metadatum"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:



        global meta_list

        metadatum_exist=False

        message = tracker.latest_message.get('text')
        print("messagio",message)




        dict_selection = {}
        for num, name in enumerate(Selection_list):
            if (name[1] == False):
                dict_selection.update({name[0]: ['False']})

            elif (name[1] == True):
                dict_selection.update({name[0]: ['True']})

            else:
                dict_selection.update({name[0]: [name[1]]})

        z = db.find_all_keys(dict_selection)
        c = {}
        for y in z:
            c.update({y: y})
            print(y)

##---------------------------------------
        c={}
        print(meta_list)
        for k, v in meta_list.items():
            print(k, v)
            print("messagio nella lista")
            print(meta_list)
            metadatum_exist= True
            c.update({v,v})
##--------------------------------------

        if (c != {}):
            if (shell == False):
                dispatcher.utter_message(Utils.choice("First 50 metadatum:", c, show_search=True))
            else:
                dispatcher.utter_message("First 50 metadatum:")
                print(c)

        return []


class ShowAllRegion(Action):

    def name(self) -> Text:
        return "action_show_all_region"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dict_selection = {}
        for num, name in enumerate(Selection_list):
            if (name[1] == False):
                dict_selection.update({name[0]: ['False']})

            elif (name[1] == True):
                dict_selection.update({name[0]: ['True']})

            else:
                dict_selection.update({name[0]: [name[1]]})

        z = db.find_regions(dict_selection,{})
        print(z)
        c = {}
        for y in z:
            c.update({y: y})
            print(y)

        if (c != {}):
            if (shell == False):
                dispatcher.utter_message(Utils.choice("First 50 region:", c, show_search=True))
            else:
                dispatcher.utter_message("First 50 region:")
                print(c)

        return []



class CheckMetaExistence(Action):

    def name(self) -> Text:
        return "action_check_metadatum_existence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global meta_list

        metadatum_exist=False

        message = tracker.latest_message.get('text')
        print("messagio",message)

        print(meta_list)
        for k, v in meta_list.items():
            print(k, v)
            print("messagio nella lista")
            if(message ==  v):
                print(meta_list)
                metadatum_exist= True

        #find all keys senza filtro aggiunto (if...)


        if(metadatum_exist == True):
            c="You are going to modify [" + message + "]. If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label'). If you want to compute its value starting from an existing metadata, please tell me the metadatum name."
            dispatcher.utter_message(c)

            d = {'True': 'true', '3': '3', 'My Label': 'My Label'}

            if (shell == False):
                dispatcher.utter_message(Utils.choice("Examples", d))

        else:
            dispatcher.utter_message("You are creating [" + message + "] metadatum. If you want to assign the same value for all the samples just digit it (e.g., 3, true, 'my label'). If you want to compute its value starting from an existing metadata, please tell me the metadatum name. ")
            d = {'True': 'true', '3': '3', 'My Label': 'My Label'}

            if (shell == False):
                dispatcher.utter_message(Utils.choice("Examples", d))

        return []

class MetadatumValue(Action):

    def name(self) -> Text:
        return "action_metadatum_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent=tracker.latest_message['intent'].get('name')

      #  if(last_intent == 'metadatum'):
        dispatcher.utter_message("Which operation do you want to do?")
        if (shell == False):
            dispatcher.utter_message(Utils.choice('Available operations', {'sum': 'sum ', 'subtract': 'subtract ','divide': 'divide ','multiply': 'multiply '}, show_search=True, show_help=True))
        return []

        #elif(last_intent == 'value'):
        #    dispatcher.utter_message("Which operation do you want to do?")
        #    if (shell == False):
        #        dispatcher.utter_message(Utils.choice('Available operations', {'sum': 'sum ', 'subtract': 'subtract ', 'divide ': 'divide', 'multiply': 'multiply'},show_search=True, show_help=True))
        #    return []

        #else:
        #    print("You have to insert a value or a metadatum")
        #    return[]


class InsertOperator(Action):

    def name(self) -> Text:
        return "action_insert_op"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent=tracker.latest_message.get('text')

        if(last_intent == 'sum' or last_intent=='+'):
            dispatcher.utter_message("Please, insert the value or the metadatum you want to add ")
            return []

        elif(last_intent == 'subtract' or last_intent=='-'):
            dispatcher.utter_message("Please, insert the value or the metadatum you want to subtract ")
            return []

        elif (last_intent == 'divide' or last_intent == '/'):
            dispatcher.utter_message("Please, insert the divider.\nIt can be either a value or a metadatum. ")
            return []

        elif (last_intent == 'multuply' or last_intent == '*'):
            dispatcher.utter_message(" Please, insert the factor.\nIt can be either a value or a metadatum ")
            return []

        else:
            print("Error in action insert operator")
            return[]


#################################################################################################
######################################  K - means  ##############################################
#################################################################################################
class ShowFeatureSample(Action):

    def name(self) -> Text:
        return "action_show_feature_sample"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_param = {'Feature': 'Feature', 'Sample': 'Sample'}

        if (shell == False):
            dispatcher.utter_message(Utils.choice("Data Types", list_param))
        else:
            dispatcher.utter_message("Options {}".format(list_param))

        return []


class ShowOperations(Action):

    def name(self) -> Text:
        return "action_show_operations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_param = {'Cluster': 'Cluster', 'Other': 'Other'}

        if (shell == False):
            dispatcher.utter_message(Utils.choice("Data Types", list_param))
        else:
            dispatcher.utter_message("Options {}".format(list_param))

        return []


class ActionTakeMinMax(Action):

    def name(self) -> Text:
        return "action_take_min_max"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global N_cluster

        last_intent=tracker.latest_message['intent'].get('name')

        if(last_intent == 'value'):
            Min_Max_values = tracker.latest_message.get('text')
            print(Min_Max_values)

            if (';' in Min_Max_values):
                c = Min_Max_values.split(';')
                min =c[0]
                print(c[0])
                max =c[1]
                print(c[1])
                KM=KMeans(3, clusters=None, tuning=True, min= min, max=max)
                print(workflow)
                workflow.add(KM)
                print(workflow)
                workflow.run(workflow[-1])

                #for i in c:
                #    print(c[i])

        return []


class ActionNClusters(Action):

    def name(self) -> Text:
        return "action_n_clusters"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Min_Max_cluster,N_cluster,Min_cluster,Max_cluster

        last_intent=tracker.latest_message['intent'].get('name')

        if(last_intent == 'value'):
            N_cluster = tracker.latest_message.get('text')
            KM=KMeans(3, clusters=N_cluster, tuning=True, min=min, max=max)
            workflow.add(KM)

            return []


class ActionGoBack(Action):

    def name(self) -> Text:
        return "action_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Min_Max_cluster, N_cluster, Min_cluster, Max_cluster

        dispatcher.utter_message("ok! let's go back")

        return [UserUtteranceReverted(),UserUtteranceReverted(), ActionReverted(), ActionReverted()] #, ActionReverted()


class ActionAddCluster(Action):

    def name(self) -> Text:
        return "action_add_cluster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global workflow

        workflow.add(Select(ds))

        return []