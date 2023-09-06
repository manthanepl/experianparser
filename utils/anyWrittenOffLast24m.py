from datetime import datetime, timedelta

def checkWriteOffStatus(CAIS_Account_DETAILS):

    """
    check whether a customer has any credit accounts that were written off (declared as non-recoverable) within the last 24 months.
    """
    twentyfour_months_ago = datetime.now() - timedelta(days=730)
    # if multiple tradelines exists
    if isinstance(CAIS_Account_DETAILS, list):
        
        # calculate number of written off loan accounts
        no_of_wo = sum(
            1
            for account in CAIS_Account_DETAILS
            if account["Written_off_Settled_Status"] != '' and int(account["Written_off_Settled_Status"])  in [2, 6, 8] and datetime.strptime(account.get("Date_Reported", ""), "%Y%m%d") > twentyfour_months_ago
        )

        # no written off  loan  accounts
        if no_of_wo == 0:
            return False
        elif no_of_wo > 0:
            return True

    # if it is a single tradeline
    # elif isinstance(CAIS_Account_DETAILS, dict):
    else:
        if CAIS_Account_DETAILS["Written_off_Settled_Status"] != '' and int(CAIS_Account_DETAILS["Written_off_Settled_Status"]) in [2, 6, 8]  and datetime.strptime(CAIS_Account_DETAILS.get("Date_Reported", ""), "%Y%m%d") > twentyfour_months_ago:
            return True
        else:
            return False
