def map_credit_facility_status(code):
    credit_facility_statuses = {
        0: 'Restructured Loan',
        1: 'Restructured Loan (Govt. Mandated)',
        2: 'Written-off', #
        3: 'Settled',
        4: 'Post (WO) Settled', 
        5: 'Account Sold',
        6: 'Written Off and Account Sold', #
        7: 'Account Purchased',
        8: 'Account Purchased and Written Off', #
        9: 'Account Purchased and Settled',
        10: 'Account Purchased and Restructured',
        11: 'Restructured due to Natural Calamity',
        12: 'Restructured due to COVID-19',
        99: 'Clear Existing Status',
        999: 'Unknown'
    }
    return credit_facility_statuses.get(code, 'Unknown')