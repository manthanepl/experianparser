from dateutil import relativedelta
from datetime import datetime

def month_diff(date1,date2):
    # print(date1,date2)
    # Calculate the difference between the two dates in months
    difference = relativedelta.relativedelta(date2, date1)
    
    # Extract the number of months from the difference
    months_difference = difference.months + (12 * difference.years)

    return months_difference

def bureauVintageMonths(CAIS_Account_DETAILS):
    """
    indicates how long an individual or entity has been using credit facilities or loans.

    bureau vintage months = current date month - oldest open date (oldest tradeline by open date)
    """
    # if multiple tradelines exists
    if isinstance(CAIS_Account_DETAILS, list):
               
        # extract open dates in datetime format and exclude the null open date values
        open_dates = [ datetime.strptime(account["Open_Date"], "%Y%m%d") for account in CAIS_Account_DETAILS if account["Open_Date"] !='' ]
        # sort the open dates from old to recent
        sorted_dates = sorted(open_dates, reverse=False)
        # select the oldest open date
        oldest_open_date =  sorted_dates[0]
        # get current date
        current_date = datetime.now()
        
        # calculate diff between current date and oldest open date
        return month_diff(oldest_open_date,current_date)
     # for single tradeline   
    # elif isinstance(CAIS_Account_DETAILS,dict):
    else:
        open_date = datetime.strptime(CAIS_Account_DETAILS['Open_Date'], "%Y%m%d")
        current_date = datetime.now()

        return month_diff(open_date,current_date)
        