import psycopg2 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_pan(input_values):
    SOURCE_DB_NAME =os.getenv('APP_SOURCE_DB_NAME')
    SOURCE_DB_USER = os.getenv('APP_SOURCE_DB_USER')
    SOURCE_DB_PASSWORD = os.getenv('APP_SOURCE_DB_PASSWORD')
    SOURCE_DB_HOST = os.getenv('APP_SOURCE_DB_HOST')
    SOURCE_DB_PORT = os.getenv('APP_SOURCE_DB_PORT')

    try:
        source_con = psycopg2.connect(dbname=SOURCE_DB_NAME, user=SOURCE_DB_USER, password=SOURCE_DB_PASSWORD, host=SOURCE_DB_HOST,port = SOURCE_DB_PORT)
        source_cursor = source_con.cursor()

        # Execute a query
        source_cursor.execute(f"SELECT ( SELECT pan FROM generic.customer WHERE id = app.customer_id) AS pan, app.id AS id FROM generic.application app WHERE app.id IN ({input_values})")
        data = source_cursor.fetchall()
        
        
        # Close the cursor and connection when done
        source_cursor.close()

        data_list =  [{"pan": row[0], "app_id": row[1]} for row in data]
        return  data_list

    except Exception as e:
        print(f"Error {e}")
    
    