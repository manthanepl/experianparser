from datetime import datetime
import datetime as dt
import pytz
from components.loan_emi_details import loan_details
from mapping.accountHolderMapping import map_account_holder_type
from mapping.collateral_mapping import map_collateral_type
from mapping.creditFacilityMapping import map_credit_facility_status
from mapping.loanTypeMapping import loanTypeMapping
from mapping.paymentFrequencyMapping import map_paymentFrequency
from mapping.securedTypeMapping import isSecured
from mapping.accountStatusMapping import isActive
from mapping.suitFiledStatusMapping import map_suit_filed_status
from utils.bureauVintageMonths import month_diff

def parse_date(date_str):
    if date_str != '':
        return datetime.strptime(date_str, "%Y%m%d")
    else:
        return None
    
def convert_repayment_tenure(repayment_tenure_str):
    if repayment_tenure_str.isdigit():
        return int(repayment_tenure_str)
    elif repayment_tenure_str == "":
        return None
    else:
        return None
    

def paymentEndDate(CAIS_Account_History):
    if isinstance(CAIS_Account_History, list):
        max_date = dt.datetime(1, 1, 1)
        for entry in CAIS_Account_History:
            year = int(entry.get("Year", 1))
            month = int(entry.get("Month", 1))
            date = dt.datetime(year, month, 1)
            max_date = max(max_date, date)
        return max_date.strftime("%Y%m%d")
    elif isinstance(CAIS_Account_History, dict):
        year = int(CAIS_Account_History.get("Year", 1))
        month = int(CAIS_Account_History.get("Month", 1))
        date = dt.datetime(year, month, 1)
        return date.strftime("%Y%m%d")
    else:
        return None




def accountDetails(bureau_data,account_holder_id,conn,cursor):
    
    if 'INProfileResponse' in bureau_data:
        CAIS_Account_DETAILS = bureau_data['INProfileResponse']['CAIS_Account']['CAIS_Account_DETAILS']

        # if customer has multiple tradelines then it is a list of dict
        if isinstance(CAIS_Account_DETAILS,list):
            for account in CAIS_Account_DETAILS:
                date_reported = parse_date(account['Date_Reported']) 
                loan_type = loanTypeMapping(int(account.get("Account_Type"))) if account.get("Account_Type","") != '' else 0
                secured  = isSecured(account.get("Account_Type",""))
                cash_credit = False  # default value
                overdraft = True if int(account.get("Account_Type","")) in [38,39,227,226] else False
                hl_lap = True if int(account.get("Account_Type","")) in [2,42,168,58,226] else False
                active = False if account.get("Date_Closed","") != '' else True
                date_opened = parse_date(account['Open_Date']) 
                start_payment_date = parse_date(account['DateOfAddition']) 
                ownership_type = map_account_holder_type(account['AccountHoldertypeCode'])
                payment_tenure_months = convert_repayment_tenure(account['Repayment_Tenure'])
                last_payment_date = parse_date(account['Date_of_Last_Payment'])
                interest_rate = round(float(account['Rate_of_Interest']),2) if account.get('Rate_of_Interest','') != '' else None
                member_shortname = "NOT DISCLOSED" # default value
                emi_amount = None # default value
                account_holder_id= account_holder_id
                collateral_type = map_collateral_type(account.get('Type_of_Collateral',''))
                payment_frequency = map_paymentFrequency(account.get('Terms_Frequency',''))
                payment_end_date = paymentEndDate(account['CAIS_Account_History'])
                high_credit_amount = float(account['Highest_Credit_or_Original_Loan_Amount']) if account.get('Highest_Credit_or_Original_Loan_Amount','') != '' else 0
                actual_payment_amount = None # not available in experian json
                payment_history = None # default value
                remaining_balance = float(account['Current_Balance']) if account.get('Current_Balance','') != '' else 0
                date_closed = parse_date(account['Date_Closed'])
                index = None # not available in experian json
                collateral_value = int(account['Value_of_Collateral']) if account.get('Value_of_Collateral','') != '' else None
                credit_card_credit_limit = float(account['Credit_Limit_Amount']) if account.get('Credit_Limit_Amount','') != '' else 0
                credit_card_cash_limit = None # not available in experian json
                account_number = account['Account_Number'] if account.get('Account_Number',"") != '' else None
                amount_overdue = None
                if 'Credit_Facility_Status' in account:
                    credit_facility_status =   map_credit_facility_status(int(account['Credit_Facility_Status'])) if account['Credit_Facility_Status'] != '' else None
                elif 'Written_off_Settled_Status' in account:
                    credit_facility_status=   map_credit_facility_status(int(account['Written_off_Settled_Status'])) if account['Written_off_Settled_Status'] != '' else None
                
                wo_amount_total = float(account['Written_Off_Amt_Total']) if account.get('Written_Off_Amt_Total','') != '' else None
                wo_amount_principal = float(account['Written_Off_Amt_Principal']) if account.get('Written_Off_Amt_Principal','') != '' else None
                suit_filed =map_suit_filed_status(account['SuitFiled_WilfulDefault']) if account.get('SuitFiled_WilfulDefault','') != '' else None
                settlement_amount = float(account['Settlement_Amount']) if account.get('Settlement_Amount','') != '' else None
                source_name = bureau_data['added_data']['bureau_source']
                source_table_id = bureau_data['added_data']['row_id']

                if 'Credit_Facility_Status' in account:
                    written_off =   True if account.get('Credit_Facility_Status','') in ['02','06','08'] and account.get('Credit_Facility_Status','') !='' else False
                elif 'Written_off_Settled_Status' in account:
                    written_off=   True if account.get('Written_off_Settled_Status','') in ['02','06','08'] and account.get('Written_off_Settled_Status','') !='' else False

                written_off_date = parse_date(account['WriteOffStatusDate'])
                loan_vintage_in_months = month_diff(date_opened,datetime.now())
                vintage_calulation_date = datetime.now()
                utc_time = datetime.now().astimezone(pytz.utc)


                account_details = {
                        "date_reported": date_reported,
                        "loan_type": loan_type,
                        "secured": secured,
                        "cash_credit": cash_credit,
                        "overdraft": overdraft,
                        "hl_lap": hl_lap,
                        "active": active,
                        "date_opened": date_opened,
                        "payment_start_date": start_payment_date,
                        "ownership_type": ownership_type,
                        "payment_tenure_in_months": payment_tenure_months,
                        "last_payment_date": last_payment_date,
                        "interest_rate": interest_rate,
                        "member_short_name": member_shortname,
                        "emi_amount": emi_amount,
                        "account_holder_id": account_holder_id,
                        "collateral_type": collateral_type,
                        "payment_frequency": payment_frequency,
                        "payment_end_date": payment_end_date,
                        "high_credit_amount": high_credit_amount,
                        "actual_payment_amount": actual_payment_amount,
                        "payment_history": payment_history,
                        "remaining_balance": remaining_balance,
                        "date_closed": date_closed,
                        "index": index,
                        "collateral_value": collateral_value,
                        "credit_card_credit_limit": credit_card_credit_limit,
                        "credit_card_cash_limit": credit_card_cash_limit,
                        "account_number": account_number,
                        "amount_overdue": amount_overdue,
                        "credit_facility_status": credit_facility_status,
                        "wo_amount_total": wo_amount_total,
                        "wo_amount_principal": wo_amount_principal,
                        "suit_filed": suit_filed,
                        "settlement_amount": settlement_amount,
                        "source_name": source_name,
                        "source_table_id": source_table_id,
                        "written_off": written_off,
                        "written_off_date": written_off_date,
                        "loan_vintage_in_months": loan_vintage_in_months,
                        "vintage_calculation_date": vintage_calulation_date,
                        #  "vintage_calculation_date_utc": utc_time
                      }
                 
                # Build the SQL query dynamically
                columns = '"'+'", "'.join(account_details.keys()) + '"  '        #"account_holder_id"'   # Double Quotes on every Column Names
                placeholders = ", ".join(["%s"] * (len(account_details)))
                values = [account_details.get(key) for key in account_details] 
                query = f"INSERT INTO veritas.cais_account_details ({columns}) VALUES ({placeholders}) RETURNING id"

                # Execute the SQL query with the values
                cursor.execute(query, values)

                # Commit the changes to the database
                conn.commit()

                loan_id = cursor.fetchone()[0]
                loan_details(account_holder_id,loan_id,account['CAIS_Account_History'],conn,cursor)

                #

                # # Print all the variables
                # print(f"date_reported: {date_reported}")
                # print(f"loan_type: {loan_type}")
                # print(f"secured: {secured}")
                # print(f"cash_credit: {cash_credit}")
                # print(f"overdraft: {overdraft}")
                # print(f"hl_lap: {hl_lap}")
                # print(f"active: {active}")
                # print(f"date_opened: {date_opened}")
                # print(f"start_payment_date: {start_payment_date}")
                # print(f"ownership_type: {ownership_type}")
                # print(f"payment_tenure_months: {payment_tenure_months}")
                # print(f"last_payment_date: {last_payment_date}")
                # print(f"interest_rate: {interest_rate}")
                # print(f"member_shortname: {member_shortname}")
                # print(f"emi_amount: {emi_amount}")
                # print(f"account_holder_id: {account_holder_id}")
                # print(f"collateral_type: {collateral_type}")
                # print(f"payment_frequency: {payment_frequency}")
                # print(f"payment_end_date: {payment_end_date}")
                # print(f"high_credit_amount: {high_credit_amount}")
                # print(f"actual_payment_amount: {actual_payment_amount}")
                # print(f"payment_history: {payment_history}")
                # print(f"remaining_balance: {remaining_balance}")
                # print(f"date_closed: {date_closed}")
                # print(f"index: {index}")
                # print(f"collateral_value: {collateral_value}")
                # print(f"credit_card_credit_limit: {credit_card_credit_limit}")
                # print(f"credit_card_cash_limit: {credit_card_cash_limit}")
                # print(f"account_number: {account_number}")
                # print(f"amount_overdue: {amount_overdue}")
                # print(f"credit_facility_status: {credit_facility_status}")
                # print(f"wo_amount_total: {wo_amount_total}")
                # print(f"wo_amount_principal: {wo_amount_principal}")
                # print(f"suit_filed: {suit_filed}")
                # print(f"settlement_amount: {settlement_amount}")
                # print(f"source_name: {source_name}")
                # print(f"source_table_id: {source_table_id}")
                # print(f"written_off: {written_off}")
                # print(f"written_off_date: {written_off_date}")
                # print(f"loan_vintage_in_months: {loan_vintage_in_months}")
                # print(f"vintage_calulation_date: {vintage_calulation_date}")

                
            # if it is a single tradeline
        elif isinstance(CAIS_Account_DETAILS,dict):
                account = CAIS_Account_DETAILS
                date_reported = parse_date(account['Date_Reported']) 
                loan_type = loanTypeMapping(int(account.get("Account_Type"))) if account.get("Account_Type","") != '' else 0
                secured  = isSecured(account.get("Account_Type",""))
                cash_credit = False  # default value
                overdraft = True if int(account.get("Account_Type","")) in [38,39,227,226] else False
                hl_lap = True if int(account.get("Account_Type","")) in [2,42,168,58,226] else False
                active = False if account.get("Date_Closed","") != '' else True
                date_opened = parse_date(account['Open_Date']) 
                start_payment_date = parse_date(account['DateOfAddition']) 
                ownership_type = map_account_holder_type(account['AccountHoldertypeCode'])
                payment_tenure_months = convert_repayment_tenure(account['Repayment_Tenure'])
                last_payment_date = parse_date(account['Date_of_Last_Payment'])
                interest_rate = round(float(account['Rate_of_Interest']),2) if account.get('Rate_of_Interest','') != '' else None
                member_shortname = "NOT DISCLOSED" # default value
                emi_amount = None # default value
                account_holder_id= account_holder_id
                collateral_type = map_collateral_type(account.get('Type_of_Collateral',''))
                payment_frequency = map_paymentFrequency(account.get('Terms_Frequency',''))
                payment_end_date = paymentEndDate(account['CAIS_Account_History'])
                high_credit_amount = float(account['Highest_Credit_or_Original_Loan_Amount']) if account.get('Highest_Credit_or_Original_Loan_Amount','') != '' else 0
                actual_payment_amount = None # not available in experian json
                payment_history = None # default value
                remaining_balance = float(account['Current_Balance']) if account.get('Current_Balance','') != '' else 0
                date_closed = parse_date(account['Date_Closed'])
                index = None # not available in experian json
                collateral_value = int(account['Value_of_Collateral']) if account.get('Value_of_Collateral','') != '' else None
                credit_card_credit_limit = float(account['Credit_Limit_Amount']) if account.get('Credit_Limit_Amount','') != '' else 0
                credit_card_cash_limit = None # not available in experian json
                account_number = account['Account_Number'] if account.get('Account_Number',"") != '' else None
                amount_overdue = None
                if 'Credit_Facility_Status' in account:
                    credit_facility_status =   map_credit_facility_status(int(account['Credit_Facility_Status'])) if account['Credit_Facility_Status'] != '' else None
                elif 'Written_off_Settled_Status' in account:
                    credit_facility_status=   map_credit_facility_status(int(account['Written_off_Settled_Status'])) if account['Written_off_Settled_Status'] != '' else None
                
                wo_amount_total = float(account['Written_Off_Amt_Total']) if account.get('Written_Off_Amt_Total','') != '' else None
                wo_amount_principal = float(account['Written_Off_Amt_Principal']) if account.get('Written_Off_Amt_Principal','') != '' else None
                suit_filed =map_suit_filed_status(account['SuitFiled_WilfulDefault']) if account.get('SuitFiled_WilfulDefault','') != '' else None
                settlement_amount = float(account['Settlement_Amount']) if account.get('Settlement_Amount','') != '' else None
                source_name = bureau_data['added_data']['bureau_source']
                source_table_id = bureau_data['added_data']['row_id']

                if 'Credit_Facility_Status' in account:
                    written_off =   True if account.get('Credit_Facility_Status','') in ['02','06','08'] and account.get('Credit_Facility_Status','') !='' else False
                elif 'Written_off_Settled_Status' in account:
                    written_off=   True if account.get('Written_off_Settled_Status','') in ['02','06','08'] and account.get('Written_off_Settled_Status','') !='' else False

                written_off_date = parse_date(account['WriteOffStatusDate'])
                loan_vintage_in_months = month_diff(date_opened,datetime.now())
                vintage_calulation_date = datetime.now()
                utc_time = datetime.now().astimezone(pytz.utc)


                account_details = {
                        "date_reported": date_reported,
                        "loan_type": loan_type,
                        "secured": secured,
                        "cash_credit": cash_credit,
                        "overdraft": overdraft,
                        "hl_lap": hl_lap,
                        "active": active,
                        "date_opened": date_opened,
                        "payment_start_date": start_payment_date,
                        "ownership_type": ownership_type,
                        "payment_tenure_in_months": payment_tenure_months,
                        "last_payment_date": last_payment_date,
                        "interest_rate": interest_rate,
                        "member_short_name": member_shortname,
                        "emi_amount": emi_amount,
                        "account_holder_id": account_holder_id,
                        "collateral_type": collateral_type,
                        "payment_frequency": payment_frequency,
                        "payment_end_date": payment_end_date,
                        "high_credit_amount": high_credit_amount,
                        "actual_payment_amount": actual_payment_amount,
                        "payment_history": payment_history,
                        "remaining_balance": remaining_balance,
                        "date_closed": date_closed,
                        "index": index,
                        "collateral_value": collateral_value,
                        "credit_card_credit_limit": credit_card_credit_limit,
                        "credit_card_cash_limit": credit_card_cash_limit,
                        "account_number": account_number,
                        "amount_overdue": amount_overdue,
                        "credit_facility_status": credit_facility_status,
                        "wo_amount_total": wo_amount_total,
                        "wo_amount_principal": wo_amount_principal,
                        "suit_filed": suit_filed,
                        "settlement_amount": settlement_amount,
                        "source_name": source_name,
                        "source_table_id": source_table_id,
                        "written_off": written_off,
                        "written_off_date": written_off_date,
                        "loan_vintage_in_months": loan_vintage_in_months,
                        "vintage_calculation_date": vintage_calulation_date,
                        # "vintage_calculation_date_utc": utc_time
                      }  



                columns = '"'+'", "'.join(account_details.keys()) + '"  '        #"account_holder_id"'   # Double Quotes on every Column Names
                placeholders = ", ".join(["%s"] * (len(account_details)))
                values = [account_details.get(key) for key in account_details] 
                query = f"INSERT INTO veritas.cais_account_details ({columns}) VALUES ({placeholders}) RETURNING id"

                # Execute the SQL query with the values
                cursor.execute(query, values)

                # Commit the changes to the database
                conn.commit()