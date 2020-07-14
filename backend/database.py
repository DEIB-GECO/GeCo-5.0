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


t_flatten_gecoagent = db.Table(
    'flatten_gecoagent',
    db.Column('item_id', db.Integer),
    db.Column('biosample_type', db.Text, index=True),
    db.Column('tissue', db.Text, index=True),
    db.Column('cell', db.Text),
    db.Column('is_healthy', db.Boolean, index=True),
    db.Column('disease', db.Text, index=True),
    db.Column('dataset_name', db.Text, index=True),
    db.Column('data_type', db.Text, index=True),
    db.Column('file_format', db.Text, index=True),
    db.Column('assembly', db.Text, index=True),
    db.Column('is_annotation', db.Boolean, index=True),
    db.Column('technique', db.Text, index=True),
    db.Column('feature', db.Text, index=True),
    db.Column('target', db.Text, index=True),
    db.Column('content_type', db.Text, index=True),
    db.Column('source', db.Text, index=True),
    schema='dw'
)


