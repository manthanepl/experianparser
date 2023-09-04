
import psycopg2 

def experian_parser(bureau_data, dest_config):
    conn = psycopg2.connect(**dest_config)
    cursor = conn.cursor()

    if 'added_data' in bureau_data:
        added_data = bureau_data['added_data']
        application_id = added_data['application_id']
        bureau_source = added_data['bureau_source']
        row_id = added_data['row_id']

        

    if 'INProfileResponse' in bureau_data:
        print("True")
