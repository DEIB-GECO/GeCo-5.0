#!/usr/bin/env bash


TABLES="flatten_gecoagent"


flask-sqlacodegen --flask --schema "dw" --tables $TABLES --outfile model_db.py postgresql+psycopg2-binary://geco:geco78@localhost/gmql_meta_new16
