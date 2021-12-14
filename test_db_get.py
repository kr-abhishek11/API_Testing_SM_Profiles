# this code is using pandas dataframe to post API response to Postgresql database


from sqlalchemy import create_engine
import io
import requests
import psycopg2
import pandas as pd
from configparser import ConfigParser
file = "config.ini"
config = ConfigParser()
config.read(file)

url_get = config['URL']['get']
resp = requests.get(url_get)
resp_data = resp.json()
#print(resp_data)
resp_data = pd.json_normalize(resp_data,max_level=10)
#df = pd.concat([pd.DataFrame(v) for k,v in resp_data.items()], keys=resp_data)

#print(df)

#df = pd.concat([pd.DataFrame(v) for k,v in resp_data.items()], k=resp_data)
df = pd.DataFrame(resp_data) #converting api json data in python dataframe
print(df)
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/test')

df.head(0).to_sql('bwtier_get_data', engine, if_exists='replace',index=False) #drops old table and creates new empty table

conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'bwtier_get_data', null="") # null values become ''
conn.commit()

 

# this code snippet is used to retrieve back the response from the DB and match with the API response

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
            url_get = config['URL']['get']
            resp = requests.get(url_get)
            resp_data = resp.json()
            for i in range(len(resp_data)):
                bw_tier_data = resp_data[i]
                bw_tier_data_list = []
                for key,value in bw_tier_data.items():
                     bw_tier_data_list.append(value)
                record_to_insert = bw_tier_data_list 
                #print(record_to_insert)       
                
            # this code snippet is used to validate the database data with the API data   
            cur.execute("SELECT * from bwtier_get_data")
            rows = cur.fetchall() #fetching all the rows from our DB
            #print(type(rows))
           # print(rows[-1]) #fetching the last row from DB after GET API call insertion
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
