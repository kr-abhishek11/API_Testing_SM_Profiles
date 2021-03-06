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
            url_put = config['URL']['put']
            print(url_put)
            resp = requests.put(url_put)
            resp_data = resp.json() 
            print(resp_data)
            bw_tier_data_list = []
            for key,value in resp_data.items():
                bw_tier_data_list.append(value)
                record_to_insert = bw_tier_data_list
            name=record_to_insert[3]
            bwtier_id=record_to_insert[0]
            # update name based on the bwtier_id
            sql = """ UPDATE bwtier_data
                        SET name = %s
                        WHERE bwtier_id = %s"""
           
            cur.execute(sql, (name,bwtier_id))
            # get the number of updated rows
            updated_rows = cur.rowcount
             # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        
            print("Number of Rows Updated ",updated_rows)

            # this code snippet is used to validate the database data after the PUT API call is done 
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
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

