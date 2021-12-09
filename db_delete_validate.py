import psycopg2
import psycopg2.extras
import requests
from bwtier_api import BW_TIER_DATA
from test_api_calls import *
from configparser import ConfigParser
file = "config.ini"
config = ConfigParser()
config.read(file)

hostname = config['DATABASE']['HOST']
database = config['DATABASE']['DB']
username = config['DATABASE']['USERNAME']
pwd = config['DATABASE']['PASSWORD']
port_id = config['DATABASE']['PORT']

conn= None
cur= None
try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id ) as conn:
        
        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
            url_delete = config['URL']['delete']
            bwtier_id = url_delete[-1] #fetching the last character from url where bwtier_id will be present
            resp = requests.delete(url_delete)
            resp_data = resp.json() 
            sql = """ DELETE from bwtier_data
                        WHERE bwtier_id = %s"""
           
            cur.execute(sql, bwtier_id)
            # get the number of updated rows
            updated_rows = cur.rowcount
             # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        
            print("Number of Rows Deleted ",updated_rows)

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

