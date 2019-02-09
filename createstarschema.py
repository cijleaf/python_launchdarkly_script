#!/usr/bin/env python
# Description:
#    Thsi script creates the star schema for database. 
# Author:
# Create Date:
# Updated By:
# Updated Date
# Change Log
import logging
import sys,os
import datetime
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2 import sql
from config import config

#############################################
# Create required STAGE, TEMP & MASTER Tables #
#############################################


def str_schema(sqlfile='home/ec2-user/py_etl/strschema.sql', debug = False):
    """ create tables in the PostgreSQL database"""
    try:
        with open(sqlfile, 'r') as f:
            rawstatements = f.read()
    except Exception as exc:
        print("Can't open {} Error: {}".format(sqlfile, exc))
        raise SystemExit

    params = params = config('/home/ec2-user/py_etl/.database.ini')
    db_params = params['etl_profile']
    vars = params['vars']
    preparedstatemnts = rawstatements.format(**vars)
    print(preparedstatemnts)

    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('SQL error: ', exc_type, exc_tb.tb_lineno)
    else:
        cur.execute(preparedstatemnts)
        conn.commit()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




if __name__ == '__main__':
    str_schema("/home/ec2-user/py_etl/strschema.sql")
print("Star schema tables were loaded successfully")