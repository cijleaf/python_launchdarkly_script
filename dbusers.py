!/usr/bin/python
import sys
import psycopg2
from psycopg2.extensions import AsIs
from config import config
import logging
import traceback

DEBUG = True

def connect():
    """ Connect to the Redshift database cluster """
    conn = None
    sql = []
    try:
        # read connection parameters
        params = config('.database.ini')
        db_params = params['redshift']
        vars = params['vars']

        if DEBUG:
            print(db_params)
            print(vars)
            print()
            sql.append("CREATE SCHEMA %s" % (vars['cstflschema']))
            sql.append("set search_path to %s" % (vars['cstflschema']))
            sql.append("CREATE USER %s WITH PASSWORD %s" % (AsIs(vars['dbetlusr']), vars['dbetlusrpswd']))
            sql.append("ALTER USER %s create db" % (AsIs(vars['dbetlusr'])))
            sql.append("CREATE USER %s WITH PASSWORD %s" % (AsIs(vars['dbappusr']), vars['dbappusrpswd']))
            sql.append("""GRANT USAGE ON SCHEMA %s TO %s""" % (AsIs(vars['cstflschema']), vars['dbappusr']))
            sql.append("""GRANT SELECT ON ALL TABLES IN SCHEMA %s TO %s""" % (AsIs(vars['cstflschema']),
                                                                              vars['dbappusr']))
            sql.append("""ALTER DEFAULT PRIVILIGES IN SCHEMA %s GRANT SELECT ON TABLES TO %s""" %
                       (AsIs(vars['cstflschema']), vars['dbappusr']))
            sql.append("""GRANT ALL ON SCHEMA %s TO %s""" % (AsIs(vars['cstflschema']), vars['dbetlusr']))
            sql.append("""GRANT ALL ON ALL TABLES IN SCHEMA %s TO %s""" % (AsIs(vars['cstflschema']),
                                                                           vars['dbetlusr']))
            sql.append("""ALTER DEFAULT PRIVILEGES IN SCHEMA %s GRANT ALL ON TABLES TO %s""" %
                       (AsIs(vars['cstflschema']), vars['dbetlusr']))
            for cmd in sql:
                print(cmd)
            print()


        # connect to the Redshift cluster
        print('Connecting to Redshift...')
        conn = psycopg2.connect(**db_params)

        # Auto commit transactions
        #conn.autocommit = True

        # create a cursor
        cur = conn.cursor()


        # check db version
        print('Redshift database version:')
        cur.execute('SELECT version()')

        # display the Redshift database server version
        db_version = cur.fetchone()
        print(db_version)

        # create schema
        #print('Creating schema...')
        cur.execute("create schema %s" % (vars['cstflschema']))

        #set search path to schema
        #cur.execute("set search_path to %s" % (AsIs(vars['cstflschema'])))

        # create required ppl db users and grant appropriate permissions
        cur.execute("CREATE USER %s WITH PASSWORD %s" % (AsIs(vars['dbetlusr']), vars['dbetlusrpswd']))
        cur.execute("ALTER USER %s createdb" % (AsIs(vars['dbetlusr'])))
        cur.execute("CREATE USER %s WITH PASSWORD %s" % (AsIs(vars['dbappusr']), vars['dbappusrpswd']))
        cur.execute("GRANT USAGE ON SCHEMA %s TO %s" % (AsIs(vars['cstflschema']), vars['dbappusr']))
        cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA %s TO %s" % (AsIs(vars['cstflschema']), vars['dbappusr']))
        cur.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA %s GRANT SELECT ON TABLES TO %s" % (AsIs(vars['cstflschema']),
                                                                                            vars['dbappusr']))

        cur.execute("GRANT ALL ON SCHEMA %s TO %s" % (AsIs(vars['cstflschema']), vars['dbetlusr']))
        cur.execute("GRANT ALL ON ALL TABLES IN SCHEMA %s TO %s" % (AsIs(vars['cstflschema']), vars['dbetlusr']))
        cur.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA %s GRANT ALL ON TABLES TO %s" % (AsIs(vars['cstflschema']),
                                                                                         vars['dbetlusr']))



        # Commit transaction
        conn.commit()
        print(cur._last_executed)
        raise

         # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno, error)
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
connect()