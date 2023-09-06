
import psycopg2 
import os
from dotenv import load_dotenv
from datetime import datetime
from components.bureauPersonDetails import bureauPersonDetails

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


def experian_parser(bureau_data):
    conn = psycopg2.connect(**dest_config)
    cursor = conn.cursor()

    person_details =bureauPersonDetails(bureau_data)

    # Create an SQL query to insert data into the table
    sql_query = f"""
        INSERT INTO veritas.bureau_person_details ({', '.join(person_details.keys())})
        VALUES ({', '.join(['%s'] * len(person_details))})
    """

    # Create a list of values to be inserted in the same order as the variable names
    values_to_insert = list(person_details.values())

    # Execute the SQL query with the values
    cursor.execute(sql_query, values_to_insert)
    account_holder_id = cursor.fetchone()[0]

    # Commit the changes to the database
    conn.commit()



    # Close the cursor and the database connection
    cursor.close()
    conn.close()