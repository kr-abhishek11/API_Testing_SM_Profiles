import psycopg2
import psycopg2.extras
import requests
from bwtier_api import BW_TIER_DATA

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
        #bw_tier_data = requests.get('http://127.0.0.1:5000/bwtier').json
        bw_tier_data = requests.get('http://127.0.0.1:5000/bwtier')
        
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                #print(type(BW_TIER_DATA))
                #print(len(BW_TIER_DATA))
                #bw_tier_data0 = BW_TIER_DATA[0]
                #bw_tier_data1 = BW_TIER_DATA[1]
                #bw_tier_data2 = BW_TIER_DATA[2]
                #bw_tier_data0_list = []
                #print(BW_TIER_DATA[2])
                for i in range(len(BW_TIER_DATA)):
                    # print(i)
                    bw_tier_data0 = BW_TIER_DATA[i]
                    #print(bw_tier_data0)
                    bw_tier_data0_list = []
                    for key,value in bw_tier_data0.items():
                        bw_tier_data0_list.append(value)
                    print(bw_tier_data0_list)
                    #print(bw_tier_data0_list)
                    bwtier_id = bw_tier_data0_list[i] 
                    name =  bw_tier_data0_list[i+1]
                    downstreamPir =bw_tier_data0_list[i+2]
                    downstreamCir =bw_tier_data0_list[i+3]
                    upstreamPir = bw_tier_data0_list[i+4]
                    upstreamCir = bw_tier_data0_list[i+5]
                    insert_script = '''INSERT INTO bw_tier_data(bwtier_id,name,downstreamPir,downstreamCir,upstreamPir,upstreamCir) VALUES(%s,%s,%s,%s,%s,%s) 
                                        '''
                   
                    cur.execute(insert_script,(str(bwtier_id),str(name),str(downstreamPir),str(downstreamCir),str(upstreamPir),str(upstreamCir)))
                conn.commit()
            

            
           

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
