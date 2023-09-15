from utils.maxDPDlast1yr import calculate_max_dpd


def GL_CC_KCC_EL_dpd_last1yr(CAIS_Account_DETAILS):
    maxdpd = 0 
    if isinstance(CAIS_Account_DETAILS,list):
        for account in CAIS_Account_DETAILS:
            if account.get("Account_Type","") in ["07","08","36","10","191","130","05","5","224"]:
                # comparedpd(max_dpd,)
                CAIS_Account_History=account['CAIS_Account_History']
                account_max_dpd = calculate_max_dpd(CAIS_Account_History)
                # if account lvl max dpd is greater than global dpd then assign new max dpd
                if account_max_dpd > maxdpd:
                    maxdpd = account_max_dpd

        return maxdpd
    elif isinstance(CAIS_Account_DETAILS,dict):
        account = CAIS_Account_DETAILS
        if account.get("Account_Type","") in  ["07","08","36","10","191","130","05","5","224"]:
            CAIS_Account_History=account['CAIS_Account_History']
            account_max_dpd = calculate_max_dpd(CAIS_Account_History)
            # if account lvl max dpd is greater than global dpd then assign new max dpd
            if account_max_dpd > maxdpd:
                maxdpd = account_max_dpd
            
        return maxdpd