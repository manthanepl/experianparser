def loanTypeMapping(acct_type):
        new_acct_type_mapping = {1: 'Auto Loan', 2: 'Housing Loan', 3: 'Property Loan',
                         4: 'Loan Against Shares/Securities', 5: 'Personal Loan',
                         6: 'Consumer Loan', 7: 'Gold Loan', 8: 'Educational Loan',
                         191: 'Gold Loan',
                         9: 'Loan To Professional', 10: 'Credit Card', 11: 'Leasing',
                         12: 'Overdraft', 13: 'Two-Wheeler Loan', 14: 'Non-Funded Credit Facility',
                         15: 'Loan Against Bank Deposits', 16: 'Fleet Card',
                         17: 'Commercial Vehicle Loan', 18: 'Telco – Wireless',
                         19: 'Telco – Broadband', 20: 'Telco – Landline', 23: 'GECL Secured', 24: 'GECL Unsecured',
                         168: 'Credit Card', 221: 'Used Car Loan', 222: 'Construction Equipment Loan',
                         34: 'Tractor Loan', 35: 'Credit Card',
                         36: 'Credit Card', 225: 'Loan On Credit Card',
                         226: 'Prime Minister Jaan Dhan Yojana - Overdraft',
                         227: 'Mudra Loans – Shishu / Kishor / Tarun', 40: 'Microfinance – Business Loan',
                         41: 'Microfinance – Personal Loan', 220: 'Microfinance – Housing Loan', 43: 'Microfinance – Others',
                         44: 'Pradhan Mantri Awas Yojana - Credit Link Subsidy Scheme MAY CLSS',
                         45: 'P2P Personal Loan', 46: 'P2P Auto Loan', 47: 'P2P Education Loan', 50: 'Business Loan - Secured',
                         51: 'Business Loan – General', 52: 'Business Loan –Priority Sector – Small Business',
                         53: 'Business Loan –Priority Sector – Agriculture',
                         54: 'Business Loan –Priority Sector – Others',
                         55: 'Business Non-Funded Credit Facility – General',
                         56: 'Business Non-Funded Credit Facility – Priority Sector – Small Business',
                         57: 'Business Non-Funded Credit Facility – Priority Sector – Agriculture',
                         58: 'Business Non-Funded Credit Facility – Priority Sector – Others',
                         59: 'Business Loans Against Bank Deposits', 60: 'Staff Loan',
                         228: 'Business Loan - Unsecured', 0: 'Other', '': ''}
    
        old_acct_type_mapping = {
            31: 'Credit Card', 
            32: 'Used Car Loan',
            33: 'Construction Equipment Loan',
            37: 'Loan On Credit Card',
            38: 'Prime Minister Jaan Dhan Yojana - Overdraft',
            39: 'Mudra Loans – Shishu / Kishor / Tarun', 
            40: 'Microfinance – Business Loan',
            42: 'Microfinance – Housing Loan'
        }
        
        if acct_type in new_acct_type_mapping:
            acct_type = new_acct_type_mapping[acct_type]
        elif acct_type in old_acct_type_mapping:
            acct_type = old_acct_type_mapping[acct_type]
        else:
            acct_type = 'Other'

        return acct_type