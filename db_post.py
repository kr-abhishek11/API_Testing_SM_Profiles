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
    
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            # Saving POST value in GET table itself
            url_post = config['URL']['post']
            resp = requests.post(url_post)
            resp_data = resp.json() 
            for i in range(len(resp_data)):
                bw_tier_data = resp_data[i]
                bw_tier_data_list = []
                for key,value in bw_tier_data.items():
                     bw_tier_data_list.append(value)
                record_to_insert = bw_tier_data_list        
                insert_script = '''INSERT INTO bwtier_data(bwtier_id,downstreamPir,downstreamCir,name,upstreamPir,upstreamCir) VALUES(%s,%s,%s,%s,%s,%s) 
                                          '''
                cur.execute(insert_script,record_to_insert)
                conn.commit()


            
           

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
