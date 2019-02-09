#!/usr/bin/env python
# Description:
#    Thsi script creates the Tables structures in Redshift for MCE MVP
# Parameters: None
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


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE {cstflschema}.{pplrfrnccnttable} (
            PRCDR_CD VARCHAR(5),
            ASC_PRDCR_FRQNCY INTEGER,
            PRIMARY KEY(PRCDR_CD)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{pplrfrncdesctable} (
                PRCDR_CD VARCHAR(5),
                PRCDR_CD_TYPE VARCHAR(10),
                PRCDR_CD_SHRT_DESC VARCHAR(250),
                PRCDR_CD_LONG_DESC VARCHAR(500),
                PRCDR_CD_FULL_DESC VARCHAR(500),
                PRCDR_CD_CNSMR_DESC VARCHAR(250),
                PRCDR_CD_CNSMR_RECMND_DESC VARCHAR(250),
                PRIMARY KEY(PRCDR_CD)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{pplstgcosttable} (
               PRCDR_CD VARCHAR(5),
               PRCDR_CD_CNSMR_DESC VARCHAR(250),
               HOSPTL_BNDL_APC_FLAG VARCHAR(25),
                AVG_HOSPTL_MDCR_APPRVD_AMT VARCHAR(15),
               AVG_ASC_MDCR_APPRVD_AMT VARCHAR(15),
               AVG_HOSPTL_TOT_MDCR_PD_AMT VARCHAR(15),
               AVG_ASC_TOT_MDCR_PD_AMT VARCHAR(15),
               AVG_HOSPTL_BENE_COPAY_AMT VARCHAR(15),
               HOSPTL_INPTNT_DDCTBL_CAP_AMT VARCHAR(15),
               AVG_ASC_BENE_COPAY_AMT VARCHAR(15),
               PRIMARY KEY(PRCDR_CD)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{ppltmpcosttable} (
               PRCDR_CD VARCHAR(5),
               PRCDR_CD_CNSMR_DESC VARCHAR(250),
               HOSPTL_BNDL_APC_FLAG VARCHAR(25),
               AVG_HOSPTL_MDCR_APPRVD_AMT NUMERIC(15,2),
               AVG_ASC_MDCR_APPRVD_AMT NUMERIC(15,2),
               AVG_HOSPTL_TOT_MDCR_PD_AMT NUMERIC(15,2),
               AVG_ASC_TOT_MDCR_PD_AMT NUMERIC(15,2),
               AVG_HOSPTL_BENE_COPAY_AMT NUMERIC(15,2),
               HOSPTL_INPTNT_DDCTBL_CAP_AMT NUMERIC(15,2),
               AVG_ASC_BENE_COPAY_AMT NUMERIC(15,2),
               DESCRPTN_DUP_CNT INTEGER,
               PRIMARY KEY(PRCDR_CD)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{pplmstrcosttable} (
                PRCDR_SK BIGINT
                ,PRCDR_CD VARCHAR(5)
                ,PRCDR_SHRT_DESC VARCHAR(250)
                ,PRCDR_LONG_DESC VARCHAR(500)
                ,PRCDR_FULL_DESC VARCHAR(500)
                ,PRCDR_CNSMR_DESC VARCHAR(500)
                ,PRCDR_CNSMR_RECMND_DESC VARCHAR(250)
                ,PRCDR_DISPLAY_DESC VARCHAR(500)
                ,HOSPTL_BNDL_APC_FLAG VARCHAR(25)
                ,AVG_HOSPTL_MDCR_APPRVD_AMT INTEGER
                ,AVG_ASC_MDCR_APPRVD_AMT INTEGER
                ,AVG_HOSPTL_TOT_MDCR_PD_AMT INTEGER
                ,AVG_ASC_TOT_MDCR_PD_AMT INTEGER
                ,AVG_HOSPTL_BENE_COPAY_AMT INTEGER
                ,AVG_ASC_BENE_COPAY_AMT INTEGER
                ,ASC_PRCDR_VOLUME INTEGER
                ,PRIMARY KEY(PRCDR_SK)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{pplprcdrdimtable} (
                     PRCDR_SK BIGINT
                ,PRCDR_CD VARCHAR(5)
                ,PRCDR_SHRT_DESC VARCHAR(250)
                ,PRCDR_LONG_DESC VARCHAR(500)
                ,PRCDR_FULL_DESC VARCHAR(500)
                ,PRCDR_CNSMR_DESC VARCHAR(500)
                ,PRCDR_CNSMR_RECMND_DESC VARCHAR(250)
                ,PRCDR_DISPLAY_DESC VARCHAR(500)
                ,HOSPTL_BNDL_APC_FLAG VARCHAR(25)
                ,PRIMARY KEY(PRCDR_SK)
        )
        """,
        """
        CREATE TABLE {cstflschema}.{pplcostfacttable} (
                 PRCDR_SK BIGINT
                 ,AVG_HOSPTL_MDCR_APPRVD_AMT INTEGER
                 ,AVG_ASC_MDCR_APPRVD_AMT INTEGER
                 ,AVG_HOSPTL_TOT_MDCR_PD_AMT INTEGER
                 ,AVG_ASC_TOT_MDCR_PD_AMT INTEGER
                 ,AVG_HOSPTL_BENE_COPAY_AMT INTEGER
                 ,AVG_ASC_BENE_COPAY_AMT INTEGER
                 ,ASC_PRCDR_VOLUME INTEGER
                 ,PRIMARY KEY(PRCDR_SK)
        )
        """)
    conn = None
    try:
        #read connection parameters
        params = config
        db_params = params['admin_profile']
        vars = params['vars']

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("set autocommit=true")
        cur.execute("set search_path to {cstflschema}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplrfrnccnttable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplrfrncdesctable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplstgcosttable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{ppltmpcosttable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplmstrcosttable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplprcdrdimtable}".format(**var))
        cur.execute("DROP TABLE IF EXISTS {cstflschema}.{pplcostfacttable}".format(**var))
        cur.execute("GRANT USAGE ON SCHEMA {cstflschema} to {dbappusr}".format(**var))
        cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA {cstflschema} TO {dbappusr}".format(**var))
        cur.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA {cstflschema} GRANT SELECT ON TABLES TO {dbappusr}".format(**var))
        cur.execute("GRANT ALL ON SCHEMA {cstflschema} TO {dbappusr}".format(**var))
        cur.execute("GRANT ALL ON ALL TABLES IN SCHEMA {cstflschema} to {dbappusr}".format(**var))
         cur.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA {cstflschema} GRANT ALL ON TABLES TO {dbappusr}".format(**var))
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
           conn.close()


if __name__ == '__main__':
    create_tables()
    print("Database tables were created successfully")

