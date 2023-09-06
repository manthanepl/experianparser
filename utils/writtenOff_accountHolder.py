def totalWrittenOffAmount(CAIS_Account_DETAILS):
    """
    represents the cumulative value of debt that has been declared uncollectible by lenders 
    """

    if isinstance(CAIS_Account_DETAILS, list):
        
        # calculate sum of written off total amount across all  loan accounts
        sum_writtenOff_total_amt = sum(
            int(account['Written_Off_Amt_Total']) if account['Written_Off_Amt_Total'] !='' else 0
            for account in CAIS_Account_DETAILS)

        # calculate sum of written off principal amount across all  loan accounts
        sum_writtenOff_principal_amt = sum(
        int(account['Written_Off_Amt_Principal']) if account['Written_Off_Amt_Principal'] !='' else 0
        for account in CAIS_Account_DETAILS)


        return sum_writtenOff_total_amt , sum_writtenOff_principal_amt

    # if it is a single tradeline
    # elif isinstance(CAIS_Account_DETAILS, dict):
    else:
        # if (CAIS_Account_DETAILS["Written_off_Settled_Status"] != '' and int(CAIS_Account_DETAILS["Written_off_Settled_Status"]) in [2, 6, 8]) or  (CAIS_Account_DETAILS["SuitFiledWillfulDefaultWrittenOffStatus"] != '' and int(CAIS_Account_DETAILS["SuitFiledWillfulDefaultWrittenOffStatus"] in [5,6,7])) :
        #     return True
        # else:
        #     return False
        writtenOff_total_amt = int(CAIS_Account_DETAILS['Written_Off_Amt_Total']) if CAIS_Account_DETAILS['Written_Off_Amt_Total'] !='' else 0
        writtenOff_principal_amt = int(CAIS_Account_DETAILS['Written_Off_Amt_Principal']) if CAIS_Account_DETAILS['Written_Off_Amt_Principal'] !='' else 0
        return writtenOff_total_amt,writtenOff_principal_amt
    