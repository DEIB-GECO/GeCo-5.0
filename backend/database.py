from sqlalchemy import BigInteger, Boolean, Column, Integer, Table, Text, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy

def get_db_uri():
    # postgres_url = get_env_variable("POSTGRES_URL")
    # postgres_user = get_env_variable("POSTGRES_USER")
    # postgres_pw = get_env_variable("POSTGRES_PW")
    # postgres_db = get_env_variable("POSTGRES_DB")
    postgres_url = "localhost"
    postgres_user = "geco_ro"
    postgres_pw = "geco78"
    postgres_db = "gmql_meta_new16"
    return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=postgres_user,
                                                                 pw=postgres_pw,
                                                                 url=postgres_url,
                                                                 db=postgres_db)

db = SQLAlchemy()

annotation_fields = ["content_type", "assembly", "source"]
experiment_fields = ['source', 'data_type', 'assembly', 'file_format', 'biosample_type', 'tissue', 'cell', 'disease', 'is_healthy', 'technique', 'feature', 'target']

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
        print(val)
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

            #print("select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) and {} group by key".format(
            #       query, query2))
            keys = db.engine.execute(
                "select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) and {} group by key".format(
                    query, query2)).fetchall()
        else:
            keys = db.engine.execute("select key, count(distinct(value)) from dw.unified_pair_gecoagent where item_id in ({}) group by key".format(query)).fetchall()
        keys = {i[0]:i[1] for i in keys}
        print(keys)
        return keys

    def find_keys(self, filter, string):
        query = self.query_field(filter)
        print(query)
        keys = db.engine.execute("select key from dw.unified_pair_gecoagent where key like '%{}%' and item_id in ({}) group by key".format(string, query)).fetchall()
        print(keys)
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
            print("select value, count(distinct(item_id)) from dw.unified_pair_gecoagent where item_id in ({}) and {} and key in ('{}') group by value".format(
                    query, query2, str(key)))
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
                print(i[0])
                number = False
        return val, number


    def download_filter_meta(self, gcm, filter2):
        filter = ' and '.join(
            [self.is_ann_gcm] + ['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 gcm.items()])
        if filter2!={}:
            query = self.query_key(filter2)
            links = db.engine.execute("select local_url  from dw.flatten_gecoagent where {} and {} group by local_url".format(filter, query)).fetchall()
        else:
            links = db.engine.execute(
                "select local_url  from dw.flatten_gecoagent where {} group by local_url".format(filter)).fetchall()

        val = [i[0] for i in links]
        print(val)
        return val


'''
    def meta_table(self, gcm):
        gcm_source = '"source": ["tcga","encode","roadmap epigenomics","1000 genomes","refseq"]'
        if 'source' not in gcm:
            filter = ','.join(
                [self.is_ann_gcm] + [gcm_source] + [
                    '\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v]))
                    for (k, v) in gcm.items()])
        else:
            filter = ','.join(
                [self.is_ann_gcm] + ['\"{}\":[{}]'.format(k, ",".join(['\"{}\"'.format(x) for x in v])) for (k, v)
                                     in
                                     gcm.items()])
        data = '{"gcm":{' + str(filter) + '},"type":"original","kv":{}}'

        response_post = requests.post(
            api_url + 'query/table?agg=true&order_col=item_source_id&order_dir=asc&rel_distance=3',
            headers=headers_post, data=data)
        val = []
        if response_post.status_code == 200:
            val.append(response_post.content.decode('utf-8').split(sep='\n'))
        return val

def generate_where_pairs(pair_query):
    searched = pair_query.keys()

    pair_join = []

    where = []
    i = 0
    for x in searched:
        kv = "kv_" + str(i)
        i += 1
        join = f" join unified_pair {kv} on it.item_id = {kv}.item_id "
        pair_join.append(join)
        items = pair_query[x]['query']
        gcm = items['gcm']
        pair = items['pairs']

        sub_where = []

        for k in gcm.keys():
            a = ""
            a += f" lower({kv}.key) = lower('{k}') and {kv}.is_gcm = true and "
            values = gcm[k]
            sub_sub_where = []
            for value in values:
                v = value.replace("'", "''")
                sub_sub_where.append(f"lower({kv}.value) = lower('{v}')")
            a += ("(" + " OR ".join(sub_sub_where) + ")")

            # print(a)
            sub_where.append(a)

        for k in pair.keys():
            a = ""
            a += f" lower({kv}.key) = lower('{k}') and {kv}.is_gcm = false and "
            values = pair[k]
            sub_sub_where = []
            for value in values:
                v = value.replace("'", "''")
                sub_sub_where.append(f"lower({kv}.value) = lower('{v}')")
            a += ("(" + " OR ".join(sub_sub_where) + ")")

            # print(a)
            sub_where.append(a)

        where.append("(" + ") OR (".join(sub_where) + ")")

    where_part = ""
    if pair_query:
        where_part = "(" + ") AND (".join(where) + ")"

    return {'where': where_part, 'join': " ".join(pair_join)}


def sql_query_generator(gcm_query, search_type, pairs_query, return_type, agg=False, field_selected="", limit=1000,
                        offset=0, order_col="item_source_id", order_dir="ASC"):
    select_part = ""
    from_part = ""
    item = " FROM dw.item it "
    dataset_join = " join dataset da on it.dataset_id = da.dataset_id "

    pairs = generate_where_pairs(pairs_query)

    pair_join = pairs['join']
    pair_where = pairs['where']

    experiment_type_join = " join experiment_type ex on it.experiment_type_id= ex.experiment_type_id"

    replicate_join = " join replicate2item r2i on it.item_id = r2i.item_id" \
                     " join dw.replicate rep on r2i.replicate_id = rep.replicate_id"

    biosample_join = " join biosample bi on rep.biosample_id = bi.biosample_id"



    # joins = [dataset_join, experiment_type_join, replicate_join, biosample_join, donor_join, case_join, project_join]


    gcm_where = generate_where_sql(gcm_query)

    where_part = ""

    if gcm_query and pair_where:
        where_part = gcm_where + " AND " + pair_where
    elif pair_where and not gcm_where:
        where_part = 'WHERE ' + pair_where
    elif gcm_where and not pair_where:
        where_part = gcm_where

    sub_where_part = ""
    group_by_part = ""
    limit_part = ""
    offset_part = ""
    order_by = ""
    if return_type == 'table':
        if agg:
            select_part = "SELECT " + ",".join(
                x.column_name for x in columns_dict_item.values() if x.table_name not in agg_tables) + " "

            select_part += "," + ','.join(
                "STRING_AGG(DISTINCT COALESCE(" + x.column_name + "::VARCHAR,'N/D'),' | ' ) as "
                + x.column_name for x in columns_dict_item.values() if x.table_name in agg_tables)
            group_by_part = " GROUP BY " + ",".join(
                x.column_name for x in columns_dict_item.values() if x.table_name not in agg_tables)

        else:
            select_part = "SELECT " + ','.join(columns_dict_item.keys()) + " "
        if limit:
            limit_part = f" LIMIT {limit} "
        if offset:
            offset_part = f"OFFSET {offset} "
        order_by = f" ORDER BY {order_col} {order_dir} "
    elif return_type == 'count-dataset':
        select_part = "SELECT da.dataset_name as name, count(distinct it.item_id) as count "
        group_by_part = " GROUP BY da.dataset_name"

    elif return_type == 'count-source':
        select_part = "SELECT pr.source as name, count(distinct it.item_id) as count "
        group_by_part = " GROUP BY pr.source"

    elif return_type == 'download-links':
        select_part = "SELECT distinct it.local_url "
        if where_part:
            sub_where_part = " AND local_url IS NOT NULL "
        else:
            sub_where_part = " WHERE local_url IS NOT NULL "

    elif return_type == 'gmql':
        select_part = "SELECT dataset_name, array_agg(file_name) "
        if where_part:
            sub_where_part = " AND local_url IS NOT NULL "
        else:
            sub_where_part = " WHERE local_url IS NOT NULL "
        group_by_part = "GROUP BY dataset_name"

    elif return_type == 'field_value':
        col = columns_dict_item[field_selected]
        column_type = col.column_type
        lower_pre = 'LOWER(' if column_type == str else ''
        lower_post = ')' if column_type == str else ''
        distinct = ""
        # if search_type == 'original':
        distinct = "distinct"
        select_part = f"SELECT {distinct} {lower_pre}{field_selected}{lower_post} as label, it.item_id as item "

    elif return_type == 'field_value_tid':
        select_part = f"SELECT distinct LOWER(label), it.item_id as item "

        if search_type == 'synonym':
            from_part += f" join synonym syn on {field_selected}_tid = syn.tid "
        elif search_type == 'expanded':
            from_part += f" join relationship_unfolded rel on {field_selected}_tid = rel.tid_descendant "
            from_part += f" join synonym syn on rel.tid_ancestor = syn.tid "
        if where_part:
            sub_where_part = " AND type <> 'RELATED' "
            if search_type == 'expanded':
                sub_where_part += f" AND rel.distance <= {rel_distance} "
        else:
            sub_where_part = " WHERE type <> 'RELATED' "
            if search_type == 'expanded':
                sub_where_part += f" AND rel.distance <= {rel_distance} "
    elif return_type == 'item_id':
        select_part = f"SELECT it.item_id "

    return select_part + from_part + where_part + sub_where_part + group_by_part + order_by + limit_part + offset_part

def generate_where_sql(gcm_query):
    sub_where = []
    where_part = ""
    if gcm_query:
        where_part = " WHERE ("

    for (column, values) in gcm_query.items():
        col = columns_dict_item[column]
        column_type = col.column_type
        lower_pre = 'LOWER(' if column_type == str else ''
        lower_post = ')' if column_type == str else ''
        syn_sub_where = []

    sub_sub_where = [f"{lower_pre}{column}{lower_post} = '{value}'" for value in values if value is not None]
    sub_sub_where_none = [f"{column} IS NULL" for value in values if value is None]
    sub_sub_where.extend(sub_sub_where_none)
    sub_sub_where.extend(syn_sub_where)
    sub_where.append(" OR ".join(sub_sub_where))

    if gcm_query:
        where_part += ") AND (".join(sub_where) + ")"
    return where_part
'''