
from datetime import datetime, timedelta

from utils.unsecured_loan_before import SecuredOrUnsecuredLoan

def checkULorGL_last12m(CAIS_Account_DETAILS):
    """
    returns Boolean if any account has Unsecured loan or Gold loan in last 12 months
    """

    twelve_months_ago = datetime.now() - timedelta(days=365)
    # if multiple tradelines exists
    if isinstance(CAIS_Account_DETAILS, list):
        
        # calculate number of written off loan accounts
        no_of_ul_gl = sum(
            1
            for account in CAIS_Account_DETAILS
            if account["Account_Type"] != '' and (int(account["Account_Type"])==7 or  SecuredOrUnsecuredLoan(account.get('Account_Type')) == 'Unsecured') and datetime.strptime(account.get("Date_Reported", ""), "%Y%m%d") > twelve_months_ago
        )

        # no written off  loan  accounts
        if no_of_ul_gl == 0:
            return False
        elif no_of_ul_gl > 0:
            return True

    # if it is a single tradeline
    # elif isinstance(CAIS_Account_DETAILS, dict):
    else:
        if CAIS_Account_DETAILS["Account_Type"] != '' and (int(CAIS_Account_DETAILS["Account_Type"]) == 7 or  SecuredOrUnsecuredLoan(CAIS_Account_DETAILS.get('Account_Type')) == 'Unsecured') and datetime.strptime(CAIS_Account_DETAILS.get("Date_Reported", ""), "%Y%m%d") > twelve_months_ago:
            return True
        else:
            return False
