import json
import requests

api_url = 'http://geco.deib.polimi.it/genosurf/api/'
headers_post = {"accept": "application/json", "Content-Type": "application/json"}

annotation_fields = ["content_type", "assembly", "source"]
experiment_fields = ['source', 'data_type', 'assembly', 'file_format', 'biosample_type', 'tissue', 'cell', 'disease', 'is_healthy', 'technique', 'feature', 'target']
# experiment_fields = ['source', 'project_name', 'source_site']

my_dict = {}

def get_values(is_ann_gcm, f):
    data = '{"gcm":{' + \
           is_ann_gcm + \
           '},"type":"original","kv":{}}'
    response_post = requests.post(api_url + 'field/' + str(f), headers=headers_post, data=data)
    if response_post.status_code == 200:
        val = json.loads(response_post.content.decode('utf-8'))['values']
        # print(val)
        values = []
        if (val != []) and (len(val) > 1):
            for i in range(len(val)):
                if val[i]['value'] != None:
                    values.append(val[i]['value'])

    else:
        values = []
    return values

for f in annotation_fields:
    values = get_values('"is_annotation":["true"]', f)
    my_dict[(True, f)] = values

for f in experiment_fields:
    values = get_values('"is_annotation":["false"]', f)
    my_dict[(False, f)] = values


class Geno_surf:

    def __init__(self, fields, is_ann):
        self.is_ann = is_ann
        self.is_ann_gcm = '"is_annotation":["true"]' if is_ann else '"is_annotation":["false"]'
        self.fields = fields
        self.get_values()

    def get_values(self):
        data = '{"gcm":{'+ \
               self.is_ann_gcm +\
               '},"type":"original","kv":{}}'
        print(data)
        self.fields_names = []
        for f in self.fields:
            values = my_dict[(self.is_ann, f)]
            if values!=[]:
                self.fields_names.append(f)
                setattr(self, (str(f) + '_db'), values)


    def update(self, gcm):
        filter = ','.join([self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k,v) in gcm.items()])
        data = '{"gcm":{'+str(filter)+'},"type":"original","kv":{}}'
        print(data)
        self.fields_names = []
        self.all_values = []
        for f in self.fields:
            response_post = requests.post(api_url + 'field/' + str(f), headers=headers_post, data=data)
            if response_post.status_code == 200:
                val = json.loads(response_post.content.decode('utf-8'))['values']
                #print('val: '+str(val))
                values = []
                if (val!=[]) and (len(val)>1):
                    self.fields_names.append(f)
                    for i in range(len(val)):
                        if val[i]['value']!= None:
                            values.append(val[i]['value'])
                            self.all_values.append(val[i]['value'])
                elif len(val)==1:
                    values = [val[0]['value']]
            else:
                values = []
            if values!=[]:
                setattr(self, (str(f) + '_db'), values)

    def retrieve_values(self, gcm, field):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"synonym","kv":{}}'
        print(data)
        response_post = requests.post(api_url + 'field/' + str(field), headers=headers_post, data=data)
        if response_post.status_code == 200:
            val = json.loads(response_post.content.decode('utf-8'))['values']
        return val

    def download(self, gcm):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"synonym","kv":{}}'
        response_post = requests.post(api_url + 'query/download?rel_distance=3', headers=headers_post, data=data)
        val = []
        if response_post.status_code == 200:
            val.append(response_post.content.decode('utf-8').split(sep='\n'))
        return val

    # Retrieves all keys based on a user input string
    def find_keys(self, gcm, string):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"synonym","kv":{}}'
        response_post = requests.post(api_url + 'pair/keys?q=' + str(string) + '&exact=false&rel_distance=3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            pairs = json.loads(response_post.content.decode('utf-8'))['pairs']
        keys = []
        for k in pairs:
            keys.append(k['key'])
        return keys

    #Retrieves all values based on a user input string
    def find_values(self, gcm, string):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"synonym","kv":{}}'
        response_post = requests.post(api_url + 'pair/values?q=' + str(string) + '&exact=false&rel_distance=3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            pairs = json.loads(response_post.content.decode('utf-8'))['pairs']
        return pairs

    def find_key_values(self, gcm, key):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"synonym","kv":{}}'
        response_post = requests.post(api_url + 'pair/' + str(key) + '/values?is_gcm = false & rel_distance = 3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            values = json.loads(response_post.content.decode('utf-8'))['pairs']
        return values

def check_existance(is_ann, fields_dict):
    fields_dict['is_annotation'] = ['true']
    data = '{"gcm":' + str(fields_dict).replace("'",'"') + ',"type":"synonym","kv":{}}'
    #print(data)
    response_post = requests.post(api_url + 'query/count?agg=false&rel_distance=3', headers=headers_post, data=data)
    if response_post.status_code == 200:
        return int(response_post.content.decode('utf-8').strip())
    else:
        print("error")


import numpy as np
c= Geno_surf(experiment_fields, False)
#c.update({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]})
'''
cell_val = c.retrieve_values( {'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'cell')
#print(cell_val)
print(len(cell_val))
cell_val_1 = [x['value'] for x in cell_val if x['count']>29]
cell_val_1 = set(cell_val_1)
cell_val_mean = [x['count'] for x in cell_val]
print('cell ' + str(len(cell_val_1)))
print('cell mean ' + str(np.median(cell_val_mean)))
print('cell mean ' + str(np.quantile(cell_val_mean,0.75)))

target_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'target')
#print(target_val)
print(len(target_val))
target_val_1 = [x['value'] for x in target_val if x['count']>28]
target_val_1 = set(target_val_1)
target_val_mean = [x['count'] for x in target_val]
print('target ' + str(len(target_val_1)))
print('target mean ' + str(np.quantile(target_val_mean,0.75)))
'''
biosample_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'biosample_type')
#print([x['value'] for x in biosample_val if x['value'] not in c.biosample_type_db])
#content_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'content_type')

data_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'data_type')

disease_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'disease')

feature_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'feature')

#platform_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'platform')

project_name_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'project_name')

tissue_val = c.retrieve_values({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}, 'tissue')

import pandas as pd
val = [x['value'] for x in disease_val if x['count']<10]
count = [x['count'] for x in disease_val if x['count']<10]
disease_df = pd.DataFrame(count,index= val)
print(disease_df)

val = [x['value'] for x in feature_val if x['count']<10]
count = [x['count'] for x in feature_val if x['count']<10]
feature_df = pd.DataFrame(count,index= val)
print(feature_df)

val = [x['value'] for x in biosample_val if x['count']<10]
count = [x['count'] for x in biosample_val if x['count']<10]
biosample_df = pd.DataFrame(count,index= val)
print(biosample_df)

val = [x['value'] for x in data_val if x['count']<10]
count = [x['count'] for x in data_val if x['count']<10]
data_df = pd.DataFrame(count,index= val)
print(data_df)

val = [x['value'] for x in tissue_val if x['count']<10]
count = [x['count'] for x in tissue_val if x['count']<10]
tissue_df = pd.DataFrame(count,index= val)
print(tissue_df)

val = [x['value'] for x in project_name_val if x['count']<10]
count = [x['count'] for x in project_name_val if x['count']<10]
project_name_df = pd.DataFrame(count,index= val)
print(project_name_df)

'''

with open('./rasa_files/cell_bigger10.txt', 'w') as f:
    for x in cell_val_1:
        f.write(str(x)+'\n')

with open('./rasa_files/target_bigger10.txt', 'w') as f:
    for x in target_val_1:
        f.write(str(x)+'\n')

with open('./rasa_files/biosample_type.txt', 'w') as f:
    for x in biosample_val:
        f.write(str(x['value'])+'\n')


with open('./rasa_files/data_type.txt', 'w') as f:
    for x in data_val:
        f.write(str(x['value'])+'\n')

with open('./rasa_files/disease.txt', 'w') as f:
    for x in disease_val:
        f.write(str(x['value'])+'\n')

with open('./rasa_files/feature.txt', 'w') as f:
    for x in feature_val:
        f.write(str(x['value'])+'\n')

with open('./rasa_files/platform.txt', 'w') as f:
    for x in platform_val:
        f.write(str(x['value'])+'\n')

with open('./rasa_files/project_name.txt', 'w') as f:
    for x in project_name_val:
        f.write(str(x['value'])+'\n')

with open('./rasa_files/tissue.txt', 'w') as f:
    for x in tissue_val:
        f.write(str(x['value'])+'\n')

#print(c.download({"source":["gencode"], "assembly":["grch38"]}))
#print(c.content_type_db)
#print(c.assembly_db)
#print(c.source_db)
#c.update(['"source":["gencode"]'])
#c.update({"source":["gencode"], "assembly":["grch38"]})
#c.update({})
#print(c.content_type_db)
#print(c.assembly_db)
#print(c.source_db)

#gcm = {"attribute":["value"]}
#check_existance(True, {"content_type":["gene"], "source":["refseq"], "assembly":['hg19']})
'''