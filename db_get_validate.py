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


            # this code snippet is used to validate the database data with the API data   
            cur.execute("SELECT * from bwtier_data")
            rows = cur.fetchall() #fetching all the rows from our DB
            print(rows[-1]) #fetching the last row from DB after GET API call insertion
            print('\n')
            print('**********MATCHES*************')
            print('\n')
            print(record_to_insert) #this variable holds the last row from our GET API call
            if record_to_insert == rows[-1]:
                print("API data is present in our DB")
            else:
                print("API data is missing from DB")

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
