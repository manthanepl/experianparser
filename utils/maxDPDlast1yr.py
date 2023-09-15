
# in last 6 months from current date and compare with the cais account history dates 
# in business loans or loan against property 
from datetime import datetime as dt, timedelta
from mapping.bl_lap import business_loan_loan_against_property

# extract max dpd of a tradeline in last 6 months 
def calculate_max_dpd(CAIS_Account_History):
    # Function to convert month and year to a datetime object
    def parse_month_year(month, year):
        return dt.strptime(f"{year}-{month}-1", "%Y-%m-%d")

    # Get the current date
    current_date = dt.now()
    twelve_months_ago = current_date - timedelta(days=365)
    if isinstance(CAIS_Account_History, list):
        # If the input is a list of entries
        # Filter data for the last 6 months
        
        filtered_data = [
            entry
            for entry in CAIS_Account_History
            if parse_month_year(entry["Month"], entry["Year"]) >= twelve_months_ago
        ]

        if not filtered_data:
            return 0  # No data in the last 6 months

        # Set a default day value as 1 for each entry in the filtered data
        for entry in filtered_data:
            entry["Day"] = "1"

        # Find the maximum dpd in the filtered data
        max_dpd = max(int(entry["Days_Past_Due"])   for entry in filtered_data if entry["Days_Past_Due"] !='')
        return max_dpd

    elif isinstance(CAIS_Account_History, dict):
        # If the input is a single entry as a dictionary
        # Check if the entry is within the last 6 months
        entry_date = parse_month_year(CAIS_Account_History["Month"], CAIS_Account_History["Year"])
        if entry_date >= twelve_months_ago:
            # Set a default day value as 1
            CAIS_Account_History["Day"] = "1"
            return int(CAIS_Account_History["Days_Past_Due"]) if CAIS_Account_History["Days_Past_Due"] != '' else 0
        else:
            return 0  # Entry is not in the last 6 months

    else:
        return 0  # Invalid input format


def maxDpdLast1yr(CAIS_Account_DETAILS):
    maxdpd = 0 
    if isinstance(CAIS_Account_DETAILS,list):
        for account in CAIS_Account_DETAILS:
            if account.get("Account_Type","") in business_loan_loan_against_property: # in business loan or loan against property
                # comparedpd(max_dpd,)
                CAIS_Account_History=account['CAIS_Account_History']
                account_max_dpd = calculate_max_dpd(CAIS_Account_History)
                # if account lvl max dpd is greater than global dpd then assign new max dpd
                if account_max_dpd > maxdpd:
                    maxdpd = account_max_dpd

        return maxdpd
    elif isinstance(CAIS_Account_DETAILS,dict):
        account = CAIS_Account_DETAILS
        if account.get("Account_Type","") in  business_loan_loan_against_property:
            # comparedpd(max_dpd,)
            CAIS_Account_History=account['CAIS_Account_History']
            account_max_dpd = calculate_max_dpd(CAIS_Account_History)
            # if account lvl max dpd is greater than global dpd then assign new max dpd
            if account_max_dpd > maxdpd:
                maxdpd = account_max_dpd
            
        return maxdpd