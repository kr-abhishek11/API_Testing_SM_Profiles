from configparser import ConfigParser
import pandas as pd
file = "config.ini"
config = ConfigParser()
config.read(file)
import psycopg2
import psycopg2.extras
import requests
from sqlalchemy import create_engine
import io

hostname = config['DATABASE']['HOST']
database = config['DATABASE']['DB']
username = config['DATABASE']['USERNAME']
pwd = config['DATABASE']['PASSWORD']
port_id = config['DATABASE']['PORT']

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id ) as conn:
    
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute('DROP TABLE IF EXISTS bwtier_data')

            url_get = config['URL']['get']
            resp = requests.get(url_get)
            resp_data = resp.json()
            #print(resp_data)
            df = pd.DataFrame(resp_data)

            # df is the dataframe
            if len(df) > 0:
                df_columns = list(df)
                # create (col1,col2,...)
                columns = ",".join(df_columns)

                # create VALUES('%s', '%s",...) one '%s' per column
                values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

                #create INSERT INTO table (columns) VALUES('%s',...)
                insert_stmt = "INSERT INTO {} ({}) {}".format(bwtier_data,columns,values)

                cur = conn.cursor()
                psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
                conn.commit()
                cur.close()

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
