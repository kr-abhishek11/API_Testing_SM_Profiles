import psycopg2
import psycopg2.extras
import requests
from bwtier_api import BW_TIER_DATA
from test_api_calls import *
from configparser import ConfigParser
file = "config.ini"
config = ConfigParser()
config.read(file)


hostname = 'localhost'
database = 'test'
username = 'postgres'
pwd = 'password'
port_id = 5432



conn= None
cur= None
try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id ) as conn:
        bw_tier_data = requests.get(config['URL']['get'])
        print(bw_tier_data)
        #bw_tier_data_post = requests.post('http://127.0.0.1:5000/bwtier/create')
        # bw_tier_data_put = requests.put('http://127.0.0.1:5000/bwtier/0')
        # bw_tier_data_delete = requests.delete('http://127.0.0.1:5000/bwtier/1')
        
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute('DROP TABLE IF EXISTS bwtier_data')

            create_script_get= '''CREATE TABLE IF NOT EXISTS bwtier_data (

                                bwtier_id int NOT NULL,
                                downstreamPir int NOT NULL ,
                                downstreamCir int NOT NULL,
                                name varchar(100) NOT NULL ,
                                upstreamPir int NOT NULL,
                                upstreamCir int NOT NULL  
    
                                )'''
            cur.execute(create_script_get)
            
            conn.commit()
            url_get = config['URL']['get']
            resp = requests.get(url_get)
            resp_data = resp.json()
            #print(resp_data)
            #print(type(resp_data)
            #print(resp_data)
            #print(resp_data[1])
            #print(BW_TIER_DATA[1])
            #print(type(BW_TIER_DATA))   
            # for i in range(len(BW_TIER_DATA)):
                # bw_tier_data = BW_TIER_DATA[i]
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
