import psycopg2 
import os
from dotenv import load_dotenv
import json

from components.experian_parser import experian_parser
# Load environment variables from .env file
load_dotenv()

load_dotenv()

# Destination DB Config
dest_host = os.getenv('DEST_HOST')
dest_name = os.getenv('DEST_DATABASE')
dest_user = os.getenv('DEST_USER')
dest_port = os.getenv('DEST_PORT')
dest_password = os.getenv('DEST_PASSWORD')

dest_config = {
    "host": dest_host,
    "database": dest_name,
    "user": dest_user,
    "password": dest_password,
    "port": dest_port
}




def getBureauReport(data_list , bureau_source_name ,limit , folder_path,):
    SOURCE_DB_NAME =os.getenv('BUREAU_SOURCE_DB_NAME')
    SOURCE_DB_USER = os.getenv('BUREAU_SOURCE_DB_USER')
    SOURCE_DB_PASSWORD = os.getenv('BUREAU_SOURCE_DB_PASSWORD')
    SOURCE_DB_HOST = os.getenv('BUREAU_SOURCE_DB_HOST')
    # SOURCE_DB_PORT = os.getenv('APP_SOURCE_DB_PORT')

    try:
        source_con = psycopg2.connect(dbname=SOURCE_DB_NAME, user=SOURCE_DB_USER, password=SOURCE_DB_PASSWORD, host=SOURCE_DB_HOST)
        source_cursor = source_con.cursor()

        application_counter = 0

        for data in data_list:
            pan_number = data['pan']
            app_id = data['app_id']
            # Construct the query
            query = f"SELECT response, id FROM bureau_data WHERE pan_number = '{pan_number}' AND bureau_source = '{bureau_source_name}' AND response IS NOT NULL ORDER BY id DESC LIMIT {limit};"

            # Execute the query
            source_cursor.execute(query)

            # Fetch the JSON responses
            response_rows = source_cursor.fetchall()

            # print(len(response_rows))

            # Save the JSON responses to files
            for row_number, row in enumerate(response_rows, start=1):
                response_json = json.loads(row[0])
                row_id = int(row[1])
                response_json['added_data'] = {"application_id": app_id, "bureau_source": bureau_source_name, "row_id": row_id}
                
                # For parsing and uploading data to DB
                experian_parser(response_json,dest_config=dest_config)

                # For making files of JSON Response

                # output_filename = f"{app_id}-{pan_number}-{bureau_source_name}-{row_number}.json"
                # file_path = os.path.join(folder_path, output_filename)
                # with open(file_path, 'w') as f:
                #     json.dump(response_json, f, indent=4)
                # print(f"JSON response {row_number} saved to {file_path}")


                application_counter += 1

        print(f"{application_counter} Applications Proccessed Successfully")
        source_con.close()
        source_cursor.close()


    except Exception as e:
        
        print(f"Error {e}")