import json 
import psycopg2 
import os
from dotenv import load_dotenv
import pandas as pd
from argparse import ArgumentParser
from utils.getPan import get_pan
from utils.getBureauReport import getBureauReport




if __name__ == "__main__":

    def get_input(prompt, default=None):
        if default:
            prompt = f"{prompt} [{default}]: "
        user_input = input(prompt).strip()
        return user_input or default


    bureau_choices = ["ex", "tu"]

    parser = ArgumentParser(description='Execute PostgreSQL query and save JSON responses to files')
    parser.add_argument('--app-number', help='Input Application ID (if multiple, values seprated by commas)')
    parser.add_argument('--bureau-source-name', choices=bureau_choices, help='Bureau Source Name ("EX" or "TU")')
    parser.add_argument('--limit', type=int, help='Limit')
    args = parser.parse_args()

    if not args.app_number:
        args.app_number = get_input("Enter Application ID (if multiple, values seprated by commas): ")

    app_id_list = args.app_number.split(',')

    args.bureau_source_name.lower()
    if args.bureau_source_name == "ex":
        args.bureau_source_name = "experian"
    elif args.bureau_source_name == "tu":
        args.bureau_source_name = "transunion"

    if not args.limit:
        args.limit = int(get_input("Enter limit: ", default="1"))


    # Remove any leading or trailing whitespace from the input elements
    app_id_list = [item.strip() for item in app_id_list]

    # Convert the input list to a comma-separated string for the SQL query
    input_values = ', '.join(["%s"] * len(app_id_list))
    

    

    # print(app_id_list)

    pan_records = get_pan(input_values=args.app_number)

    # Fetching the script directory path
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Fetching the Folder Path to store All Bureau Reports
    folder_name = "bureau_reports_json"
    folder_path = os.path.join(script_directory, folder_name)

    # Create the folder if it doesn't exist already
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)



    # print(pan_records)


    report = getBureauReport(pan_records , args.bureau_source_name , args.limit ,folder_path)