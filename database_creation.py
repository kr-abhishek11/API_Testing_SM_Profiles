import psycopg2
import psycopg2.extras

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
    
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        
            cur.execute('DROP TABLE IF EXISTS bw_tier_data')

            create_script= '''CREATE TABLE IF NOT EXISTS bw_tier_data (

                                bwtier_id int NOT NULL,
                                name varchar(100) NOT NULL ,
                                downstreamPir int NOT NULL ,
                                downstreamCir int NOT NULL,
                                upstreamPir int NOT NULL,
                                upstreamCir int NOT NULL  
    
                                )'''
            cur.execute(create_script)
            
            conn.commit()

    

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
