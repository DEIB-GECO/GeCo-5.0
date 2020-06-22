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
        gcm = {"source": ["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]}
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
        print(data)
        self.fields_names = []
        for f in self.fields:
            values = my_dict[(self.is_ann, f)]
            if values!=[]:
                self.fields_names.append(f)
                setattr(self, (str(f) + '_db'), values)


    def update(self, gcm):
        gcm_source =  '"source": ["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]'
        if 'source' not in gcm:
            filter = ','.join([self.is_ann_gcm] + [gcm_source] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k,v) in gcm.items()])
        else:
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
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
        #print(data)
        response_post = requests.post(api_url + 'field/' + str(field), headers=headers_post, data=data)
        if response_post.status_code == 200:
            val = json.loads(response_post.content.decode('utf-8'))['values']
        return val

    def download(self, gcm):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
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
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
        response_post = requests.post(api_url + 'pair/keys?q=' + str(string) + '&exact=false&rel_distance=3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            pairs = json.loads(response_post.content.decode('utf-8'))['pairs']
        #keys = []
        #for k in pairs:
        #    keys.append(k['key'])
        #return
        return pairs

    #Retrieves all values based on a user input string
    def find_values(self, gcm, string):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
        response_post = requests.post(api_url + 'pair/values?q=' + str(string) + '&exact=false&rel_distance=3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            pairs = json.loads(response_post.content.decode('utf-8'))['pairs']
        return pairs

    def find_key_values(self, gcm, key):
        filter = ','.join(
            [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'
        print(data)
        response_post = requests.post(api_url + 'pair/' + str(key) + '/values?is_gcm=false&rel_distance=3', headers=headers_post, data=data)
        if response_post.status_code == 200:
            values = json.loads(response_post.content.decode('utf-8'))
            print('VALUES')
            print(values)
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



#c= Geno_surf(experiment_fields, False)
#c.update({'source':["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]})
