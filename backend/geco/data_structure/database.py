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


db_string = get_db_uri()
db = create_engine(db_string)

annotation_fields = ["content_type", "assembly", "source", 'dataset_name']
experiment_fields = ['source', 'data_type', 'assembly', 'tissue', 'cell', 'disease', 'is_healthy', 'target',
                     'dataset_name']
fields = ["content_type", 'source', 'data_type', 'tissue', 'cell', 'disease', 'is_healthy', 'target', 'dataset_name',
          'assembly']
sources = ['tcga', 'encode', 'roadmap epigenomics', '1000 genomes', 'refseq']
datasets = ['grch38_tcga_gene_expression_2019_10', 'grch38_tcga_somatic_mutation_masked_2019_10',
            'grch38_tcga_methylation_2019_10', 'grch38_tcga_copy_number_masked_2019_10',
            'grch38_tcga_copy_number_2019_10',
            'grch38_tcga_mirna_expression_2019_10', 'hg19_tcga_cnv', 'hg19_tcga_rnaseq_exon', 'hg19_tcga_dnaseq',
            'hg19_tcga_mirnaseq_mirna',
            'hg19_tcga_mirnaseq_isoform', 'hg19_tcga_rnaseq_spljxn', 'hg19_tcga_rnaseq_gene''hg19_tcga_dnamethylation']
region_datasets = datasets
all_datasets = ['grch38_tcga_gene_expression_2019_10', 'grch38_tcga_somatic_mutation_masked_2019_10',
                'grch38_tcga_methylation_2019_10', 'grch38_tcga_copy_number_masked_2019_10',
                'grch38_tcga_mirna_expression_2019_10', 'hg19_tcga_rnaseqv2_isoform', 'grch38_encode_broad_2020_01',
                'hg19_roadmap_epigenomics_dmr', 'hg19_tcga_rnaseqv2_spljxn',
                'hg19_tcga_rnaseq_spljxn', 'hg19_roadmap_epigenomics_bed', 'hg19_roadmap_epigenomics_narrow',
                'hg19_tcga_mirnaseq_isoform', 'grch38_annotation_refseq', 'hg19_tcga_rnaseq_gene',
                'grch38_annotation_gencode', 'hg19_tcga_rnaseqv2_exon', 'hg19_tads_aiden',
                'hg19_roadmap_epigenomics_rna_expression', 'hg19_tcga_rnaseqv2_gene', 'hg19_tcga_cnv',
                'hg19_tcga_rnaseq_exon',
                'hg19_annotation_refseq', 'hg19_tcga_mirnaseq_mirna', 'hg19_roadmap_epigenomics_broad',
                'hg19_tcga_dnaseq', 'grch38_encode_narrow_2020_01', 'hg19_annotation_gencode',
                'hg19_roadmap_epigenomics_gapped', 'hg19_encode_broad_2020_01',
                'hg19_tads_dixon', 'hg19_tcga_dnamethylation', 'hg19_encode_narrow_2020_01',
                'grch38_tcga_mirna_isoform_expression_2019_10']

other_datasets = ['grch38_tcga_gene_expression_2019_10', 'grch38_tcga_somatic_mutation_masked_2019_10',
                  'grch38_tcga_methylation_2019_10', 'grch38_tcga_copy_number_masked_2019_10',
                  'grch38_tcga_mirna_expression_2019_10', 'grch38_encode_broad_2020_01', 'hg19_roadmap_epigenomics_dmr',
                  'hg19_tcga_rnaseq_spljxn', 'hg19_roadmap_epigenomics_bed', 'hg19_roadmap_epigenomics_narrow',
                  'hg19_tcga_mirnaseq_isoform', 'grch38_annotation_refseq', 'hg19_tcga_rnaseq_gene',
                  'grch38_annotation_gencode', 'hg19_roadmap_epigenomics_rna_expression', 'hg19_tcga_cnv',
                  'hg19_tcga_rnaseq_exon',
                  'hg19_annotation_refseq', 'hg19_tcga_mirnaseq_mirna', 'hg19_roadmap_epigenomics_broad',
                  'hg19_tcga_dnaseq', 'grch38_encode_narrow_2020_01', 'hg19_annotation_gencode',
                  'hg19_roadmap_epigenomics_gapped', 'hg19_encode_broad_2020_01',
                  'hg19_tcga_dnamethylation', 'hg19_encode_narrow_2020_01',
                  'grch38_tcga_mirna_isoform_expression_2019_10']


class database:
    def __init__(self):
        self.fields = fields
        self.get_all_values()

    # and dataset_name in {}
    def get_all_values(self):
        self.fields_names = []
        self.values = {}
        res = db.engine.execute("select item_id, local_url, donor_source_id, " + ', '.join(fields)
                                + " from dw.flatten_gecoagent where source in {} and dataset_name in {}".format(
            tuple(sources), tuple(datasets)))
        values = res.fetchall()
        self.table = pd.DataFrame(values, columns=res.keys())

        for f in self.fields:
            res = list(set(self.table[f]))
            if res != [] and len(res) > 1:
                self.fields_names.append(f)
                self.values[f] = res
                setattr(self, (str(f) + '_db'), res)
            else:
                self.table = self.table.drop(f, axis=1)

        meta = db.engine.execute("select distinct(key) from dw.unified_pair_gecoagent group by key")
        self.meta_schema = meta.fetchall()
        self.meta_schema = [i[0] for i in self.meta_schema]


class DB:
    def __init__(self, fields, is_ann, all_db):
        self.is_ann = is_ann
        self.is_ann_gcm = 'is_annotation=true' if is_ann else 'is_annotation=false'
        # self.fields = fields
        self.db = all_db
        self.table = self.db.table.copy()
        # self.table = self.table[self.table['is_annotation']==self.is_ann]
        self.fields = [i for i in self.table.columns.values if
                       i != 'item_id' and len(list(set(self.table[i].values))) > 1 and i in self.db.fields]
        self.values = {x: set(self.table[x].values) for x in fields if
                       (x in self.table.columns.values) and len(set(self.table[x].values)) > 1}
        self.fields_names = list(self.values.keys())
        self.meta_schema = self.db.meta_schema

    def update(self, gcm):
        self.all_values = []
        self.fields_names = []

        for f in gcm:
            if f != 'is_healthy':
                self.table = self.table[self.table[f].isin(gcm[f])]
            else:
                print(gcm[f])

        for f in self.fields:
            values = []
            val = list(filter(lambda x: x is not None, list(set(self.table[f]))))
            if (val != []) and (len(val) > 1):
                self.fields_names.append(f)
                for i in range(len(val)):
                    if val[i] != None:
                        values.append(val[i])
                        self.all_values.append(val[i])
            elif len(val) == 1:
                values = [val[0]]

            if values != []:
                self.values[f] = values

    def update_donors(self, ds, donors):
        self.table = self.table[self.table['dataset_name'] == ds]
        self.table = self.table[self.table['donor_source_id'].isin(donors)]

    def retrieve_values(self, gcm, f):
        values = list(self.table[f])
        set_val = list(set(values))
        set_val = list(filter(lambda x: x is not None, set_val))
        val = [{"value": i, "count": values.count(i)} for i in set_val]
        return val

    def check_existance(self, gcm):
        for f in gcm:
            self.table = self.table[self.table[f].isin(gcm[f])]
        if len(self.table) > 0:
            return len(self.table)
        else:
            print("error")
            return 0

    def download(self, gcm, donors=[]):
        if len(donors) == 0:
            links = list(set(self.table['local_url']))
        else:
            links = list(set(self.table[self.table['donor_source_id'].isin(donors)]['local_url']))
        return links

    def go_back(self, gcm):
        self.table = self.db.table.copy()
        for f in gcm:
            self.table = self.table[self.table[f].isin(gcm[f])]

    def query_field(self, gcm):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        query = "join dw.flatten_gecoagent as df on rr.item_id = df.item_id where {}".format(filter)
        return query

    def query_key(self, gcm):
        query = ""
        i = 1
        for k in gcm:
            if i < len(gcm):
                query += "item_id in (select item_id from dw.unified_pair_gecoagent where key='{}' and value in {}) and ".format(
                    k, ['{}'.format(x) for x in gcm[k]]).replace('[', '(').replace(']', ')')
            else:
                query += "item_id in (select item_id from dw.unified_pair_gecoagent where key='{}' and value in {})".format(
                    k, ['{}'.format(x) for x in gcm[k]]).replace('[', '(').replace(']', ')')
            i += 1
        return query

    def query_key2(self, gcm, items):
        for k in gcm.keys():
            print(
                "select distinct(item_id),  from dw.unified_pair_gecoagent where item_id in {} and key='{}' and value in {}".format(
                    items, k, ['{}'.format(x) for x in gcm[k]]).replace('[', '(').replace(']', ')'))
            items = db.engine.execute(
                "select distinct(item_id) from dw.unified_pair_gecoagent where item_id in ({}) and key='{}' and value in {}".format(
                    items, k, ['{}'.format(x) for x in gcm[k]]).replace('[', '(').replace(']', ')')).fetchall()
            # items = [i[0] for i in items]
            items = ','.join(str(i[0]) for i in items)
        # items = items.split(',')
        return items

    def retrieve_donors(self, meta):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        if meta != {}:
            items = self.query_key2(meta, items)
        items = items.split(',')
        items = [int(i) for i in items]
        # items = ','.join(str(i) for i in items)
        print(items)
        donors = list(self.table[self.table['item_id'].isin(items)]['donor_source_id'].values)
        return donors

    # Retrieves all keys
    def find_all_keys(self, filter, filter2={}):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)

        if filter2 != {}:
            items = self.query_key2(filter2, items)

            # keys = db.engine.execute("select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) and {} group by key".format(query, query2)).fetchall()
            keys = db.engine.execute(
                "select item_id, key, value from dw.unified_pair_gecoagent where item_id in ({})".format(
                    items)).fetchall()
        else:
            keys = db.engine.execute(
                "select item_id, key, value from dw.unified_pair_gecoagent where item_id in ({})".format(
                    items)).fetchall()
            # keys = db.engine.execute("select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) group by key".format(query)).fetchall()
            # keys = db.engine.execute("select item_id, key, value from dw.unified_pair_gecoagent where item_id in ({})".format(query)).fetchall()
        # print("select rr.item_id, rr.key, rr.value from dw.unified_pair_gecoagent as rr {}".format(
        #        query))
        # keys = db.engine.execute(
        # "select rr.item_id, rr.key, rr.value from dw.unified_pair_gecoagent as rr {}".format(
        #  query)).fetchall()

        self.metadata = pd.DataFrame(keys, columns=['item_id', 'key', 'value'])
        self.metadata = self.metadata[self.metadata['item_id'].isin(item_id)]
        set_keys = list(set(self.metadata['key']))
        keys = {i: len(set(self.metadata[self.metadata['key'] == i]['value'].values)) for i in set_keys if
                len(set(self.metadata[self.metadata['key'] == i]['value'].values)) > 1}
        return keys

    def update_meta(self, filter2):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        items = self.query_key2(filter2, items)
        items = items.split(',')
        self.table = self.table[self.table['item_id'].isin(items)]

    def find_keys(self, filter, string):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        keys = db.engine.execute(
            "select rr.key from dw.unified_pair_gecoagent as rr where item_id in ({}) and key like '%{}%' group by key".format(
                items, string)).fetchall()

        keys = [i[0] for i in keys]
        return keys

    # Retrieves all values based on a user input string
    def find_values(self, filter, string):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        values = db.engine.execute(
            "select distinct(key), value  from dw.unified_pair_gecoagent where item_id in ({}) and value like '%{}%'".format(
                items, string)).fetchall()

        val = [{"key": i[0], "value": i[1]} for i in values]
        return val

    def find_key_values(self, key, filter, filter2={}):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        if filter2 != {}:
            items = self.query_key2(filter2, items)
            values = db.engine.execute(
                "select value, count(distinct(item_id)) from dw.unified_pair_gecoagent where item_id in ({}) and key in ('{}') group by value".format(
                    items, str(key))).fetchall()
        else:
            # values = db.engine.execute("select value, count(distinct(item_id)) from dw.unified_pair_gecoagent where item_id in ({}) and key in ('{}') group by value".format(query, str(key))).fetchall()
            values = db.engine.execute(
                "select rr.value, count(distinct(rr.item_id)) from dw.unified_pair_gecoagent as rr where item_id in ({}) and rr.key in ('{}') group by value".format(
                    items, str(key))).fetchall()

        val = [{"value": i[0], "count": i[1]} for i in values]
        number = True
        for i in values:
            if str(i[0]).isnumeric() != True and i[0] != None:
                number = False
        return val, number

    def download_filter_meta(self, gcm, filter2):
        item_id = list(self.table['item_id'].values)
        items = ','.join(str(i) for i in item_id)
        if filter2 != {}:
            items = self.query_key2(filter2, items)
            items = ','.join(str(i) for i in items)
        links = db.engine.execute(
            "select local_url from dw.flatten_gecoagent where item_id in ({}) group by local_url".format(
                items)).fetchall()
        val = [i[0] for i in links]
        return val

    def find_regions(self, gcm, filter2):
        ds_name = gcm['dataset_name'][0]
        if ds_name in region_datasets:
            item_id = list(self.table['item_id'].values)
            items = ','.join(str(i) for i in item_id)
            if filter2 != {}:
                items = self.query_key2(filter2, items)
            res = db.engine.execute(
                "select * from rr.{} where (item_id in ({}))limit 1".format(ds_name,
                                                                            items))
            self.region_schema = res.keys()
        else:
            self.region_schema = None
        return self.region_schema

    '''
     def update1(self, gcm):
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
                self.values[f]=values
                #setattr(self, (str(f) + '_db'), values)



    def retrieve_values1(self, gcm, f):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        val = db.engine.execute("select {}, count({}) from dw.flatten_gecoagent where {} group by {}".format(f, f, filter, f)).fetchall()

        val = [{"value":i[0],"count":i[1]} for i in val]

        return val

    def check_existance1(self, gcm):
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

    def download1(self, gcm):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])

        links = db.engine.execute(
            "select local_url  from dw.flatten_gecoagent where {} group by local_url".format(filter)).fetchall()
        val = [i[0] for i in links]
        return val'''