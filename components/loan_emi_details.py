from datetime import datetime

def emi_type(code):
    if code == "S":
        return "Standard"
    elif code == "M":
        return "Special Mention Account"
    elif code == "B":
        return "Substandard"
    elif code == "DBT":
        return "Doubtful"
    elif code == "L":
        return "Loss"
    elif code in ["XXX", "?"]:
        return "Not Reported"
    else:
        return None

def loan_details(account_holder_id,loan_id,CAIS_Account_History,conn,cursor):
    if isinstance(CAIS_Account_History,list):
        for entry in CAIS_Account_History:
            dpd = int(entry['Days_Past_Due']) if  entry['Days_Past_Due'] != '' else 0
            year , month = entry['Year'] , entry['Month']
            date = datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")
            payment_status = emi_type(entry['Asset_Classification'])

            history = {
                'loan_id':loan_id,
                'account_holder_id':account_holder_id,
                'emi_dpd':dpd,
                'date':date,
                'payment_status':payment_status
            }
            # Build the SQL query dynamically
            columns = '"'+'", "'.join(history.keys()) + '"  '        #"account_holder_id"'   # Double Quotes on every Column Names
            placeholders = ", ".join(["%s"] * (len(history)))
            values = [history.get(key) for key in history] 
            query = f"INSERT INTO veritas.cais_account_details ({columns}) VALUES ({placeholders}) RETURNING id"

            # Execute the SQL query with the values
            cursor.execute(query, values)

            # Commit the changes to the database
            conn.commit()



    elif isinstance(CAIS_Account_History,dict):
        entry = CAIS_Account_History
        dpd = int(entry['Days_Past_Due']) if  entry['Days_Past_Due'] != '' else 0
        year , month = entry['Year'] , entry['Month']
        date = datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")
        payment_status = emi_type(entry['Asset_Classification'])

        history = {
            'loan_id':loan_id,
            'account_holder_id':account_holder_id,
            'emi_dpd':dpd,
            'date':date,
            'payment_status':payment_status
        }
        # Build the SQL query dynamically
        columns = '"'+'", "'.join(history.keys()) + '"  '        #"account_holder_id"'   # Double Quotes on every Column Names
        placeholders = ", ".join(["%s"] * (len(history)))
        values = [history.get(key) for key in history] 
        query = f"INSERT INTO veritas. ({columns}) VALUES ({placeholders}) RETURNING id"

        # Execute the SQL query with the values
        cursor.execute(query, values)

        # Commit the changes to the database
        conn.commit()