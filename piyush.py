import os, re
import psycopg2
import json
from dotenv import load_dotenv
from argparse import ArgumentParser
from datetime import datetime, timedelta

# Determine the environment (dev or prod)
environment = os.getenv("ENVIRONMENT", "dev")  # Default to dev if ENVIRONMENT is not set
env_file = ".env.dev" if environment == "dev" else ".env.prod"

# Load environment variables from .env file
load_dotenv(env_file)

# Database connection parameters for Bureau Reports
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_port = os.getenv('DB_PORT')
db_password = os.getenv('DB_PASSWORD')

# Database connection parameters for PAN Records
db_host2 = os.getenv('DB_HOST-2')
db_name2 = os.getenv('DB_NAME-2')
db_user2 = os.getenv('DB_USER-2')
db_port2 = os.getenv('DB_PORT-2')
db_password2 = os.getenv('DB_PASSWORD-2')

account_type_dict = {
    "01": "Auto Loan (Personal)",
    "02": "Housing Loan",
    "03": "Property Loan",
    "04": "Loan Against Shares/Securities",
    "05": "Personal Loan",
    "06": "Consumer Loan",
    "07": "Gold Loan",
    "08": "Education Loan",
    "09": "Loan to Professional",
    "10": "Credit Card",
    "11": "Leasing",
    "12": "Overdraft",
    "13": "Two-wheeler Loan",
    "14": "Non-Funded Credit Facility",
    "15": "Loan Against Bank Deposits",
    "16": "Fleet Card",
    "17": "Commercial Vehicle Loan",
    "18": "Telco – Wireless",
    "19": "Telco – Broadband", 
    "20": "Telco – Landline",
    "21": "Seller Financing",
    "22": "Seller Financing Soft",
    "23": "GECL Loan Secured",
    "24": "GECL Loan Unsecure",
    "31": "Secured Credit Card",
    "32": "Used Car Loan",
    "33": "Construction Equipment Loan",
    "34": "Tractor Loan",
    "35": "Corporate Credit Card",
    "36": "Kisan Credit Card",
    "37": "Loan on Credit Card",
    "38": "Prime Minister Jaan Dhan Yojana - Overdraft",
    "39": "Mudra Loans – Shishu / Kishor / Tarun",
    "40": "Microfinance – Business Loan",
    "41": "Microfinance – Personal Loan",
    "42": "Microfinance – Housing Loan",
    "43": "Microfinance – Other",
    "44": "Pradhan Mantri Awas Yojana - Credit Link Subsidy Scheme MAY CLSS",
    "45": "P2P Personal Loan",
    "46": "P2P Auto Loan",
    "47": "P2P Education Loan",
    "50": "Business Loan – Secured",
    "51": "Business Loan – General",
    "52": "Business Loan – Priority Sector – Small Business",
    "53": "Business Loan – Priority Sector – Agriculture",
    "54": "Business Loan – Priority Sector – Others",
    "55": "Business Non-Funded Credit Facility – General",
    "56": "Business Non-Funded Credit Facility – Priority Sector – Small Business",
    "57": "Business Non-Funded Credit Facility – Priority Sector – Agricultur",
    "58": "Business Non-Funded Credit Facility – Priority Sector-Others",
    "59": "Business Loan Against Bank Deposits",
    "61": "Business Loan - Unsecured",
    "80": "Microfinance Detailed Report",
    "81": "Summary Report",
    "88": "Locate Plus for Insurance",
    "90": "Account Review",
    "91": "Retro Enquiry",
    "92": "Locate Plus",
    "97": "Adviser Liability",
    "00": "Other",
    "98": "Secured",
    "99": "Unsecured"
}

ownership_indicator_dict = {
    1: "Individual",
    2: "Authorised User",
    3: "Guarantor",
    4: "Joint"
}

id_type_dict = {
    1 : "Income Tax ID Number (PAN)",
    2 : "Passport Number",
    3 : "Voter ID Number",
    4 : "Driver’s License Number",
    5 : "Ration Card Number",
    6 : "Universal ID Number (UID)",
    7 : "Additional ID #1 (For FutureUse)",
    8 : "Additional ID #2 (For FutureUse)",
}

collateral_type_dict = {
    "00" : "No Collateral",
    "01" : "Property",
    "02" : "Gold",
    "03" : "Shares",
    "04" : "Saving Account and Fixed Deposit"
}

credit_facility_type_dict = {
    "00" : "Restructured Loan",
    "01" : "Restructured Loan (Govt. Mandated)",
    "02" : "Written-off",
    "03" : "Settled",
    "04" : "Post (WO) Settled",
    "05" : "Account Sold",
    "06" : "Written Off and Account Sold",
    "07" : "Account Purchased",
    "08" : "Account Purchased and Written Off",
    "09" : "Account Purchased and Settled",
    "10" : "Account Purchased and Restructured",
    "11" : "Restructured due to Natural Calamity",
    "12" : "Restructured due to COVID-19"
}

suit_filed_dict = {
    "00" : "No Suit Filed",
    "01" : "Suit filed",
    "02" : "Wilful default",
    "03" : "Suit filed (Wilful default)"
}

written_off_dict = {
    "Written-off","Written Off and Account Sold","Account Purchased and Written Off"
}

secured_loans = {
    "Auto Loan (Personal)","Housing Loan","Property Loan","Loan Against Shares/Securities","Gold Loan","Gold Loan","Two-wheeler Loan","Non-Funded Credit Facility", "Loan Against Bank Deposits", "Commercial Vehicle Loan", "Secured Credit Card", "Used Car Loan", "Construction Equipment Loan","Tractor Loan","Microfinance – Business Loan","Microfinance – Personal Loan", "Microfinance – Housing Loan", "Microfinance – Others", "Pradhan Mantri Awas Yojana - Credit Link Subsidy Scheme MAY CLSS", "P2P Auto Loan", "Business Loan – Secured", "Business Loan – General", "Business Loan – Priority Sector – Small Business","Business Loan – Priority Sector – Agriculture", "Business Loan – Priority Sector – Others", "Business Non-Funded Credit Facility – General", "Business Non-Funded Credit Facility – Priority Sector – Small Business", "Business Non-Funded Credit Facility – Priority Sector – Agriculture", "Business Non-Funded Credit Facility – Priority Sector – Others", "Business Loan Against Bank Deposits"
}
    
cash_credit_loans = {

}
    
overdraft_loans = {
"OverDraft","Prime Minister Jaan Dhan Yojana - Overdraft"
}

# Home Loans or Loan Against Properties 
hl_lap_loans = {
"Housing Loan","Microfinance – Housing Loan","Property Loan"
}


driving_license_pattern = r'^[A-Z]{2}[0-9]{10}$'
pan_card_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
voter_card_pattern = r'^[A-Z]{3}[0-9]{7}$'
uid_pattern = r'^[0-9]{12}$'

load_dotenv(dotenv_path=".env.dev")

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

# profile_response  = data['INProfileResponse']
# name = profile_response['NameSegment']['Name']
# dob = profile_response['NameSegment']['DateOfBirth']

def dateparser_dmy(date_string):
    date_object = datetime.strptime(date_string, '%d%m%Y').date()
    date_string = date_object.strftime('%Y-%m-%d')
    return date_string



def transunion_parser(bureau_data, dest_db_params):

    conn = psycopg2.connect(**dest_db_params)
    cursor = conn.cursor()

    if 'added_data' in bureau_data:
        added_data = bureau_data['added_data']
        application_id = added_data['application_id']
        bureau_source = added_data['bureau_source']
        row_id = added_data['row_id']

    print(f"===== Starting for Application ID -> {application_id} =====")

    if 'consumerCreditData' in bureau_data:
        # General Account Data
        name_section = bureau_data.get('consumerCreditData',{})[0].get('names',{})[0]

        name = name_section.get('name',0)
        birthDate = name_section.get('birthDate',0)
        if birthDate:
            birthDate = dateparser_dmy(birthDate)
        gender = name_section.get('gender',0)
        if gender == "1":
            gender = "Female"
        if gender == "2":
            gender = "Male"
        if gender == "3":
            gender = "Transgender"
                
        today = datetime.today()
        dob_object = datetime.strptime(birthDate, '%Y-%m-%d')
        age = today.year - dob_object.year - ((today.month, today.day) < (dob_object.month, dob_object.day))

        # Bureau Scores and Date
        scores = bureau_data.get('consumerCreditData',{})[0].get('scores',{})[0]
        bureau_score = scores.get('score',0)
        bureau_score_date = scores.get('scoreDate',0)
        if bureau_score_date:
            bureau_score_date = dateparser_dmy(bureau_score_date)

        # 01 : "Income Tax ID Number (PAN)"
        # 02 : "Passport Number"
        # 03 : "Voter ID Number"
        # 04 : "Driver’s License Number"
        # 05 : "Ration Card Number"
        # 06 : "Universal ID Number (UID)"
        # 07 : "Additional ID #1 (For FutureUse)"
        # 08 : "Additional ID #2 (For FutureUse)"
        ids = bureau_data.get('consumerCreditData',{})[0].get('ids',{})
        drivers, pan, voters, uid, passport, ration = None, None, None, None, None, None
        for id in ids:
            if "idType" in id:
                id_type = int(id['idType'])
                if id_type == 1:
                    pan = id['idNumber']
                elif id_type == 2:
                    passport = id['idNumber']
                elif id_type == 3:
                    voters = id['idNumber']
                elif id_type == 4:
                    drivers = id['idNumber']
                elif id_type == 5:
                    ration = id['idNumber']
                elif id_type == 6:
                    uid = id['idNumber']
                else:
                    print("ID Not Found")


        query = """INSERT INTO veritas.bureau_person_details (
            name, date_of_birth, age, gender, bureau_score, score_date, pan, voter_id, drivers_id, uid, passport_id, ration_id, application_id, enquiry_6months, enq_calculation_datetime, any_unsecured_loan_before, parsed_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        
        account_holder_data = (
            name,
            birthDate,
            age,
            gender, 
            bureau_score,
            bureau_score_date,
            pan,
            voters,
            drivers,
            uid,
            passport,
            ration,
            application_id,
            None,
            None,
            None,
            today
        )
        
        cursor.execute(query, account_holder_data)
        inserted_id = cursor.fetchone()[0]
        conn.commit()

        print("===== Account Holder data inserted successfully =====")


        # query = """INSERT INTO cais_account_details(
        #     "dateReported", id, "accountType", "dateOpened", "paymentStartDate", "ownershipIndicator", "paymentTenure", "lastPaymentDate", "interestRate", "memberShortName", "emiAmount", "collateralType", "paymentFrequency", "paymentEndDate", "actualPaymentAmount", "highCreditAmount", "paymentHistory", "currentBalance", "dateClosed", index, account_holder_id)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        # """

        # CAIS Account Data
        accounts = bureau_data.get('consumerCreditData',{})[0].get('accounts',{})
        constant_foreign_key = inserted_id
        any_unsecured_loan = False
        write_off_in_24months = False
        write_off_amount_principal = 0
        write_off_amount_total = 0
        dates_within_six_months_counter = 0
        # Loop through the JSON data and insert into the database
        for data in accounts:
            data['source_name'] = bureau_score
            data['row_id'] = row_id
            data['source_name'] = bureau_source

            if "accountType" in data:
                account_type = data['accountType']
                if account_type in account_type_dict:
                    data['accountType'] = account_type_dict[account_type]
                else:
                    data['accountType'] = "N/A"
                
                if data['accountType'] in secured_loans:
                    data['secured'] = True
                else:
                    data['secured'] = False
                    any_unsecured_loan = True
                
                if data['accountType'] in cash_credit_loans:
                    data['cash_credit'] = True
                else:
                    data['cash_credit'] = False

                if data['accountType'] in overdraft_loans:
                    data['overdraft'] = True
                else:
                    data['overdraft'] = False

                if data['accountType'] in hl_lap_loans:
                    data['hl_lap'] = True
                else:
                    data['hl_lap'] = False

                data['loanType'] = data.pop('accountType')

            if "collateralType" in data:
                collateral_type = data['collateralType']
                if collateral_type in collateral_type_dict:
                    data['collateralType'] = collateral_type_dict[collateral_type]
                else:
                    data['collateralType'] = "N/A"

            if "suitFiled" in data:
                suit_filed_type = data['suitFiled']
                if suit_filed_type in suit_filed_dict:
                    data['suitFiled'] = suit_filed_dict[suit_filed_type]
                else:
                    data['suitFiled'] = "N/A"


            if "creditFacilityStatus" in data:
                credit_facility_status = data['creditFacilityStatus']
                if credit_facility_status in credit_facility_type_dict:
                    data['creditFacilityStatus'] = credit_facility_type_dict[credit_facility_status]
                else:
                    data['creditFacilityStatus'] = "N/A"

            if "paymentHistory" in data:
                data['paymentHistory'] = None
                
            if "dateClosed" in data:
                data['active'] = False
            else:
                data['active'] = True

            if "ownershipIndicator" in data:
                ownership = data['ownershipIndicator']
                if ownership in ownership_indicator_dict:
                    data['ownership_type'] = ownership_indicator_dict[ownership]
                    data.pop('ownershipIndicator')
                else:
                    data['ownership_type'] = "N/A"
                    data.pop('ownershipIndicator')

            if "currentBalance" in data:
                data['remainingBalance'] = data.pop('currentBalance')

            if "paymentTenure" in data:
                data['paymentTenure_in_months'] = data.pop('paymentTenure')

            if "creditLimit" in data:
                data['credit_card_creditLimit'] = data.pop('creditLimit')

            if "cashLimit" in data:
                data['credit_card_cashLimit'] = data.pop('cashLimit')
            
            # Convert date strings to date format
            date_fields = ["dateOpened", "lastPaymentDate", "dateClosed", "dateReported", "paymentStartDate", "paymentEndDate"]
            for field in date_fields:
                if field in data:
                    data[field] = datetime.strptime(data[field], '%d%m%Y').date()

            # Changing the startDate and endDate as they are reversed in JSON Data
            data['paymentStartDate'], data['paymentEndDate'] = data['paymentEndDate'], data['paymentStartDate']

            diff_years = today.year - data['dateOpened'].year
            diff_months = today.month - data['dateOpened'].month

            # Adjust the difference if months are negative
            if diff_months < 0:
                diff_years -= 1
                diff_months += 12

            data['loan_vintage_in_months'] = diff_years*12 + diff_months
            data['vintage_calculation_date'] = today.date()

            two_years_ago = today.replace(year=today.year - 2).date()
            if "paymentEndDate" in data and "creditFacilityStatus" in data:
                if data['creditFacilityStatus'] in written_off_dict:
                    data['written_off'] = True
                    if "lastPaymentDate" in data:
                        data['written_off_date'] = data['lastPaymentDate']
                    else:
                        data['written_off_date'] = data['paymentEndDate']
                        if data['written_off_date'] >= two_years_ago:
                            write_off_in_24months = True
                            write_off_amount_principal = data.get('woAmountPrincipal',0)
                            write_off_amount_total = data.get('woAmountTotal',0)
                else:
                    data['written_off'] = False
            else:
                data['written_off'] = False
            # Build the SQL query dynamically
            columns = '"'+'", "'.join(data.keys()) + '", "account_holder_id"'   # Double Quotes on every Column Names
            placeholders = ", ".join(["%s"] * (len(data) + 1))
            values = [data.get(key) for key in data] + [constant_foreign_key]
            query = f"INSERT INTO veritas.cais_account_details ({columns}) VALUES ({placeholders})"

            # Execute the query and commit
            cursor.execute(query, values)
            conn.commit()
        
        print("===== CAIS Account Details inserted Successfully =====")

        # Enquiries Account Data
        enquiries = bureau_data.get('consumerCreditData',{})[0].get('enquiries',{})
        constant_foreign_key = inserted_id
        dates_within_six_months_counter_unsecured = 0

        # Loop through the JSON data and insert into the database
        for data in enquiries:

            if "enquiryPurpose" in data:
                account_type = data['enquiryPurpose']
                if account_type in account_type_dict:
                    data['enquiryPurpose'] = account_type_dict[account_type]
                else:
                    data['enquiryPurpose'] = "N/A"
                
                if data['enquiryPurpose'] in secured_loans:
                    data['secured'] = True
                else:
                    data['secured'] = False

            # Convert date strings to date format
            date_fields = ["enquiryDate"]
            for field in date_fields:
                if field in data:
                    date_string = data[field]
                    date_obj = datetime.strptime(date_string, '%d%m%Y').date()
                    data[field] = date_obj
                    six_months_ago = datetime.now().date() - timedelta(days=180)
                    if date_obj >= six_months_ago:
                        dates_within_six_months_counter += 1
                    if data['secured'] == "False":
                        dates_within_six_months_counter_unsecured += 1

                    
            
            # Build the SQL query dynamically
            columns = '"'+'", "'.join(data.keys()) + '", "account_holder_id"'   # Double Quotes on every Column Names
            placeholders = ", ".join(["%s"] * (len(data) + 1))
            values = [data.get(key) for key in data] + [constant_foreign_key]
            query = f"INSERT INTO veritas.enquiries_details ({columns}) VALUES ({placeholders})"

            # Execute the query and commit
            cursor.execute(query, values)
            conn.commit()
        
        print("===== Enquiry Details inserted Successfully =====")
        


        query = f"""
                UPDATE veritas.bureau_person_details SET enquiry_6months = {dates_within_six_months_counter}, enquiry_6months_unsecured = {dates_within_six_months_counter_unsecured}, enq_calculation_datetime = '{today}', any_unsecured_loan_before = {any_unsecured_loan}, any_written_off_in_last_24months = {write_off_in_24months}, written_off_principal_amount = {write_off_amount_principal}, written_off_total_amount = {write_off_amount_total} WHERE id = {constant_foreign_key}
                """
        cursor.execute(query)
        conn.commit()
        print("===== Account Holder Details Updated =====")

        print("===== Application Proccessed Successfully =====")
        print("")

    else:
        raise Exception("No 'ConsumerCreditData' Found in the Data")

    # Close the cursor and connection
    cursor.close()
    conn.close()



def get_input(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    user_input = input(prompt).strip()
    return user_input or default

bureau_choices = ["ex", "tu"]

# Get input from the user or command-line arguments
parser = ArgumentParser(description='Execute PostgreSQL query and save JSON responses to files')
parser.add_argument('--app-number', help='Input Application ID (if multiple, values seprated by commas)')
parser.add_argument('--bureau-source-name', choices=bureau_choices, help='Bureau Source Name ("EX" or "TU")')
parser.add_argument('--limit', type=int, help='Limit')
args = parser.parse_args()

if not args.app_number:
    args.app_number = get_input("Enter Application ID (if multiple, values seprated by commas): ")

if not args.bureau_source_name:
    while True:
        bureau_input = get_input("Enter Bureau Source Name ('EX' or 'TU'): ")
        if bureau_input is not None:
            bureau_input = bureau_input.lower()
            if bureau_input in bureau_choices:
                args.bureau_source_name = bureau_input
                break
            else:
                print("Invalid input. Please enter 'ex' or 'tu'.")
        else:
            print("Invalid input. Please enter 'ex' or 'tu'.")
    
args.bureau_source_name.lower()
if args.bureau_source_name == "ex":
    args.bureau_source_name = "experian"
elif args.bureau_source_name == "tu":
    args.bureau_source_name = "transunion"

if not args.limit:
    args.limit = int(get_input("Enter limit: ", default="1"))


# Connecting to Database for PAN Records
conn2 = psycopg2.connect(host=db_host2, port=db_port2, dbname=db_name2, user=db_user2, password=db_password2)
cursor2 = conn2.cursor() 

app_id_list = args.app_number.split(',')

# Remove any leading or trailing whitespace from the input elements
app_id_list = [item.strip() for item in app_id_list]

# Convert the input list to a comma-separated string for the SQL query
input_values = ', '.join(["%s"] * len(app_id_list))

# Query for fetching PAN Records, Application ID from Application ID
query = f"""SELECT ( SELECT pan FROM customer WHERE id = app.customer_id) AS pan, app.id AS id FROM application app WHERE app.id IN ({input_values});"""

# Execute the query
cursor2.execute(query, app_id_list)

# Fetch the JSON responses
pan_app_data = cursor2.fetchall()

# Storing PAN Numbers as well as App ID mapped with it
data_list =  [{"pan": row[0], "app_id": row[1]} for row in pan_app_data]

# Fetching the script directory path
script_directory = os.path.dirname(os.path.abspath(__file__))

# Fetching the Folder Path to store All Bureau Reports
folder_name = "bureau_reports_json"
folder_path = os.path.join(script_directory, folder_name)

# Create the folder if it doesn't exist already
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Connect to the database for Bureau Reports
conn1 = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cursor1 = conn1.cursor()

application_counter = 0

for data in data_list:
    pan_number = data['pan']
    app_id = data['app_id']
    # Construct the query
    query = f"SELECT response, id FROM bureau_data WHERE pan_number = '{pan_number}' AND bureau_source = '{args.bureau_source_name}' AND response IS NOT NULL ORDER BY id DESC LIMIT {args.limit};"

    # Execute the query
    cursor1.execute(query)

    # Fetch the JSON responses
    response_rows = cursor1.fetchall()

    # Save the JSON responses to files
    for row_number, row in enumerate(response_rows, start=1):
        response_json = json.loads(row[0])
        row_id = int(row[1])
        response_json['added_data'] = {"application_id": app_id, "bureau_source": args.bureau_source_name, "row_id": row_id}
        # For parsing and uploading data to DB
        transunion_parser(response_json, dest_config)

        # For making files of JSON Response

        # output_filename = f"{app_id}-{pan_number}-{args.bureau_source_name}-{row_number}.json"
        # file_path = os.path.join(folder_path, output_filename)
        # with open(file_path, 'w') as f:
        #     json.dump(response_json, f, indent=4)
        # print(f"JSON response {row_number} saved to {file_path}")
        application_counter += 1

print(f"{application_counter} Applications Proccessed Successfully")

# Close the database connection
cursor1.close()
conn1.close()
cursor2.close()
conn2.close()
