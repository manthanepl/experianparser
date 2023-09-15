# check if the account type is a business loan or loan against property 
# then check if the account's account history  has any Asset classification in D,M,L or IN
# written_off_and_settled_loans = {
#     "Written-off",
#     "Settled",
#     "Post (WO) Settled",
#     "Written Off and Account Sold",
#     "Account Purchased and Written Off",
#     "Account Purchased and Settled"
# }
#  then increment counter by 1 
from datetime import datetime, timedelta
from mapping.bl_lap import business_loan_loan_against_property

def parse_date(date_str):
    if date_str != '':
        return datetime.strptime(date_str, "%Y%m%d")
    else:
        return None
    

def paymentEndDate(CAIS_Account_History):
    if isinstance(CAIS_Account_History, list):
        max_date = datetime(1, 1, 1)
        for entry in CAIS_Account_History:
            year = int(entry.get("Year", 1))
            month = int(entry.get("Month", 1))
            date = datetime(year, month, 1)
            max_date = max(max_date, date)
        return max_date.strftime("%Y%m%d")
    elif isinstance(CAIS_Account_History, dict):
        year = int(CAIS_Account_History.get("Year", 1))
        month = int(CAIS_Account_History.get("Month", 1))
        date = datetime(year, month, 1)
        return date.strftime("%Y%m%d")
    else:
        return None


def check_asset_classification(cais_history_data):
    # Function to convert month and year to a datetime object
    def parse_month_year(month, year):
        return datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")

    # Get the current date
    current_date = datetime.now()

    if isinstance(cais_history_data, list):
        # If the input is a list of entries
        # Filter data for the last 2 years
        two_years_ago = current_date - timedelta(days=365 * 2)
        filtered_data = [
            entry
            for entry in cais_history_data
            if parse_month_year(entry["Month"], entry["Year"]) >= two_years_ago
        ]

        # Set a default day value as 1 for each entry in the filtered data
        for entry in filtered_data:
            entry["Day"] = "1"

        for entry in filtered_data:
            if entry.get("Asset_Classification") in ["L", "M", "D"]:
                return 1  # Found a matching classification, return 1

        return 0  # No matching classification found, return 0

    elif isinstance(cais_history_data, dict):
        # If the input is a single entry as a dictionary
        entry_date = parse_month_year(cais_history_data["Month"], cais_history_data["Year"])
        two_years_ago = current_date - timedelta(days=365 * 2)
        if entry_date >= two_years_ago:
            # Set a default day value as 1
            cais_history_data["Day"] = "1"
            if cais_history_data.get("Asset_Classification") in ["L", "M", "D"]:
                return 1  # Found a matching classification, return 1
        return 0  # No matching classification found or entry is older than 2 years, return 0

    else:
        return 0  # Invalid input format, return 0

def checkWrittenOffsettled2y(account):
    two_years_ago = datetime.now() - timedelta(days=365 * 2)
    if account.get("Date_of_Last_Payment","")!= '':
        if parse_date(account["Date_of_Last_Payment"]) >= two_years_ago:
           if account.get("Written_off_Settled_Status","") in ["02","03","04","06","08","09"]:
               return 1
           else: 
               return 0
        else:
            return 0
    else:
        last_payment = parse_date(paymentEndDate(account['CAIS_Account_History']))
        if last_payment >= two_years_ago:
            if account.get("Written_off_Settled_Status","") in ["02","03","04","06","08","09"]:
                return 1
            else:
                return 0
        else:
            return 0 



def othersDpdLast2y(CAIS_Account_DETAILS):
    count = 0
    if isinstance(CAIS_Account_DETAILS, list): 
        for account in CAIS_Account_DETAILS:
            if account.get("Account_Type","") in business_loan_loan_against_property: # in business loan or loan against property
                if  checkWrittenOffsettled2y(account) or check_asset_classification(account['CAIS_Account_History']) :
                    count = count + 1
        
        return count 
    elif isinstance(CAIS_Account_DETAILS, dict):
        account = CAIS_Account_DETAILS
        if account.get("Account_Type","") in business_loan_loan_against_property:# in business loan or loan against property
                if  checkWrittenOffsettled2y(account) or check_asset_classification(account['CAIS_Account_History']) :
                    count = count + 1
        return count 
    

CAIS_Account_DETAILS= [
        {
            "AccountHoldertypeCode": "1",
            "LitigationStatusDate": "",
            "Open_Date": "20150226",
            "Account_Type": "53",
            "Income": "",
            "Subscriber_comments": "",
            "CurrencyCode": "INR",
            "CAIS_Holder_Details": {
                "Income_TAX_PAN": "AWRPS5052P",
                "Surname_Non_Normalized": "NARENDRA CHHALURAM DHARRA",
                "Alias": "",
                "Gender_Code": "1",
                "Date_of_birth": "19680616",
                "First_Name_Non_Normalized": "",
                "Voter_ID_Number": "",
                "Middle_Name_1_Non_Normalized": "CHHALURAM",
                "Middle_Name_3_Non_Normalized": "",
                "Middle_Name_2_Non_Normalized": "",
                "Passport_Number": "",
            },
            "Payment_History_Profile": "0000000?000000?0000?0???????????????",
            "Portfolio_Type": "I",
            "DateOfAddition": "20160905",
            "Payment_Rating": "0",
            "Value_of_Collateral": "",
            "Occupation_Code": "",
            "Subscriber_Name": "XXXX",
            "Credit_Limit_Amount": "",
            "SuitFiled_WilfulDefault": "",
            "Written_off_Settled_Status": "02",
            "Written_Off_Amt_Total": "",
            "Promotional_Rate_Flag": "",
            "CAIS_Account_History": [
                {
                    "Days_Past_Due": "0",
                    "Month": "06",
                    "Asset_Classification": "?",
                    "Year": "2018",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "05",
                    "Asset_Classification": "?",
                    "Year": "2018",
                },
                {
                    "Days_Past_Due": "33",
                    "Month": "04",
                    "Asset_Classification": "?",
                    "Year": "2023",
                },
                {
                    "Days_Past_Due": "334",
                    "Month": "04",
                    "Asset_Classification": "?",
                    "Year": "2023",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "02",
                    "Asset_Classification": "?",
                    "Year": "2018",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "01",
                    "Asset_Classification": "?",
                    "Year": "2018",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "12",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "11",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "09",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "08",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "07",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "06",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "05",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "04",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "321",
                    "Month": "02",
                    "Asset_Classification": "S",
                    "Year": "2022",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "01",
                    "Asset_Classification": "?",
                    "Year": "2017",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "12",
                    "Asset_Classification": "L",
                    "Year": "2016",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "11",
                    "Asset_Classification": "?",
                    "Year": "2016",
                },
                {
                    "Days_Past_Due": "0",
                    "Month": "09",
                    "Asset_Classification": "?",
                    "Year": "2016",
                },
            ],
        }
    ]


dpd = othersDpdLast2y(CAIS_Account_DETAILS)

print(dpd)