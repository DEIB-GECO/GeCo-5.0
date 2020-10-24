from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd

def get_db_uri():
    postgres_url = "localhost"
    postgres_user = "geco_ro"
    postgres_pw = "geco78"
    postgres_db = "gmql_meta_new16_geco_agent"
    return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=postgres_user,
                                                                 pw=postgres_pw,
                                                                 url=postgres_url,
                                                                 db=postgres_db)

#db = SQLAlchemy()
db_string = get_db_uri()
db = create_engine(db_string)

annotation_fields = ["content_type", "assembly", "source"]
experiment_fields = ['source', 'data_type', 'assembly', 'file_format', 'biosample_type', 'tissue', 'cell', 'disease', 'is_healthy', 'technique', 'feature', 'target']

class ExperimentDB():
    def __init__(self):
        is_ann_gcm = 'is_annotation=false'
        #res = db.engine.execute("select * from dw.flatten_gecoagent".format(is_ann_gcm))
        #self.original = pd.DataFrame(res.fetchall())
        #self.original.columns = res.keys()
        #self.filtered = self.original.copy()

    def filter(self, gcm):
        for x in gcm.keys():
            self.filtered = self[self[x]==gcm[x]]

#exp_db = ExperimentDB()

class AnnotationDB():
    def __init__(self):
        is_ann_gcm = 'is_annotation=true'
        res = db.engine.execute("select * from dw.flatten_gecoagent".format(is_ann_gcm))
        self.original = pd.DataFrame(res.fetchall())
        self.original.columns = res.keys()
        self.filtered = self.original.copy()

    def filter(self, gcm):
        for x in gcm.keys():
            self.filtered = self[self[x] == gcm[x]]

    def fields_names(self):
        col = []
        for x in self.filtered.columns:
            if len(set(self.filtered[x]))>1:
                col.append(x)
        return col

    def check_existance(self, gcm):
        self.filter(gcm)
        return len(self.filtered)

#ann_db = AnnotationDB()

class DB:
    def __init__(self, fields, is_ann):
        self.is_ann = is_ann
        self.is_ann_gcm = 'is_annotation=true' if is_ann else 'is_annotation=false'
        self.fields = fields
        self.get_values(self.is_ann)

    def get_values(self, is_ann):
        self.fields_names = []
        for f in self.fields:
            res = db.engine.execute("select {} from dw.flatten_gecoagent where {} group by {}".format(f,self.is_ann_gcm,f)).fetchall()
            res = [i[0] for i in res]
            if res!=[]:
                self.fields_names.append(f)
                setattr(self, (str(f) + '_db'), res)


    def update(self, gcm):
        gcm_source = "source in ('tcga','encode','roadmap epigenomics','1000 genomes','refseq')"
        if 'source' not in gcm:
            filter = ' and '.join(
                [self.is_ann_gcm] + [gcm_source] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v]))
                                                    for (k, v) in gcm.items()])
        else:
            filter = ' and '.join(
                [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                     gcm.items()])

        self.fields_names = []
        self.all_values = []
        for f in self.fields:
            val = db.engine.execute("select {} from dw.flatten_gecoagent where {} group by {}".format(f, filter, f)).fetchall()
            val = [i[0] for i in val]
            values = []
            if (val != []) and (len(val) > 1):
                self.fields_names.append(f)
                for i in range(len(val)):
                    if val[i] != None:
                        values.append(val[i])
                        self.all_values.append(val[i])
            elif len(val) == 1:
                values = [val[0]]

            if values != []:
                setattr(self, (str(f) + '_db'), values)


    def retrieve_values(self, gcm, f):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        val = db.engine.execute("select {}, count({}) from dw.flatten_gecoagent where {} group by {}".format(f, f, filter, f)).fetchall()

        val = [{"value":i[0],"count":i[1]} for i in val]

        return val

    def check_existance(self, gcm):
        filter = ' and '.join(
                [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                     gcm.items()])
        val = db.engine.execute(
            "select count(*) from dw.flatten_gecoagent where {} ".format(filter)).fetchall()

        if val[0][0]>0:
            return val[0][0]
        else:
            print("error")
            return 0

    def download(self, gcm):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])

        links = db.engine.execute(
            "select local_url  from dw.flatten_gecoagent where {} group by local_url".format(filter)).fetchall()
        val = [i[0] for i in links]
        return val

    def query_field(self, gcm):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])

        query= "select item_id from dw.flatten_gecoagent where {} group by item_id".format(filter)
        return query

    def query_key(self, gcm):
        query=""
        i = 1
        for k in gcm:
            if i<len(gcm):
                query += "item_id in (select item_id from dw.unified_pair_gecoagent where key='{}' and value in {} group by item_id) and ".format(k, ['{}'.format(x) for x in gcm[k]]).replace('[','(').replace(']',')')
            else:
                query += "item_id in (select item_id from dw.unified_pair_gecoagent where key='{}' and value in {} group by item_id)".format(k, ['{}'.format(x) for x in gcm[k]]).replace('[','(').replace(']',')')
            i+=1
        return query

    # Retrieves all keys based on a user input string
    def find_all_keys(self, filter, filter2={}):
        query = self.query_field(filter)
        if filter2!={}:
            query2 = self.query_key(filter2)
            keys = db.engine.execute(
                "select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) and {} group by key".format(
                    query, query2)).fetchall()
        else:
            keys = db.engine.execute("select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) group by key".format(query)).fetchall()
        keys = {i[0]:i[1] for i in keys}
        return keys

    def find_keys(self, filter, string):
        query = self.query_field(filter)
        keys = db.engine.execute("select key from dw.unified_pair_gecoagent where key like '%{}%' and item_id in ({}) group by key".format(string, query)).fetchall()
        keys = [i[0] for i in keys]
        return keys

    # Retrieves all values based on a user input string
    def find_values(self, filter, string):
        query = self.query_field(filter)
        values = db.engine.execute(
            "select distinct(key), value  from dw.unified_pair_gecoagent where item_id in ({}) and value like '%{}%'".format(query, string)).fetchall()
        val = [{"key":i[0],"value":i[1]} for i in values]
        return val

    def find_key_values(self, key, filter, filter2={}):
        query = self.query_field(filter)
        if filter2!={}:
            query2 = self.query_key(filter2)
            values = db.engine.execute(
                "select value, count(distinct(item_id)) from dw.unified_pair_gecoagent where item_id in ({}) and {} and key in ('{}') group by value".format(
                    query, query2, str(key))).fetchall()
        else:
            values = db.engine.execute(
                "select value, count(distinct(item_id)) from dw.unified_pair_gecoagent where item_id in ({}) and key in ('{}') group by value".format(query, str(key))).fetchall()
        val = [{"value": i[0], "count": i[1]} for i in values]
        number = True
        for i in values:
            if str(i[0]).isnumeric()!=True and i[0]!=None:
                number = False
        return val, number

    def download_filter_meta(self, gcm, filter2):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        if filter2!={}:
            query = self.query_key(filter2)
            links = db.engine.execute("select local_url from dw.flatten_gecoagent where {} and {} group by local_url".format(filter, query)).fetchall()
        else:
            links = db.engine.execute(
                "select local_url  from dw.flatten_gecoagent where {} group by local_url".format(filter)).fetchall()

        val = [i[0] for i in links]
        return val

    def retrieve_schema(self, table_name):
        region_table = 'rr.' + table_name
        print("select * from {} limit 1".format(region_table))
        region_schema = db.engine.execute("select * from {} limit 1".format(region_table)).fetchall()

            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        print(region_schema)
        region_schema = db.engine.execute("select * from {} limit 1".format(region_table))

        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        print(region_schema.keys())
        #print([col for col in region_schema.keys()])

        return region_schema

