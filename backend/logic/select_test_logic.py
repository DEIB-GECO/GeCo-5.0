#from data_structure.database import db
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


class SelectLogic:
    def __init__(self, select):
        self.op = select
        self.ds = self.op.depends_on
        self.run()

    def run(self):
        filter = ' and '.join(['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in self.op.depends_on.fields.items()])
        res = db.engine.execute("select * from rr.gene_expression_hg19 where item_id in (select item_id from dw.flatten_gecoagent where {})".format(filter))
        values = res.fetchall()
        x = pd.DataFrame(values, columns = res.keys())
        self.ds.add_region_table(x)
        self.ds.add_region_schema(list(res.keys()))
        self.op.result = self.ds
        self.op.executed = True

