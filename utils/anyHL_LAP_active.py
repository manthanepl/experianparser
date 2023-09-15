
# 2 : "Housing Loan", 42 : "Microfinance – Housing Loan", 3 : "Property Loan"

from mapping.closedaccount import closed_account


def checkFor_HL_LAP_active(CAIS_Account_DETAILS):
    """
    returns Bool for any tradeline account is active and has housing loan or loan against property
    """

 # if multiple tradelines exists
    if isinstance(CAIS_Account_DETAILS, list):
        
        # calculate number of written off loan accounts
        no_of_hl_lap_running = sum(
            1
            for account in CAIS_Account_DETAILS
            if account["Account_Type"] != '' and int(account["Account_Type"])  in [2, 42, 3,58,168,195] and closed_account(account["Date_Closed"]) ==0)

        # no written off  loan  accounts
        if no_of_hl_lap_running == 0:
            return False
        elif no_of_hl_lap_running > 0:
            return True
        # for account in CAIS_Account_DETAILS:
        #     if account["Account_Type"] != '' and int(account["Account_Type"])  in [2, 42, 3] and closed_account(account["Date_Closed"]) ==0


    # if it is a single tradeline
    # elif isinstance(CAIS_Account_DETAILS, dict):
    else:
        if CAIS_Account_DETAILS["Account_Type"] != '' and int(CAIS_Account_DETAILS["Account_Type"])  in [2, 42, 3,58,168,195] and closed_account(CAIS_Account_DETAILS["Date_Closed"]) ==0:
            return True
        else:
            return False
