def isActive(acct_status):
    if acct_status in (11, 21, 22, 23, 24, 25, 71, 78, 80, 82, 83, 84):
        acct_status = 'ACTIVE'
    elif acct_status in (12, 13, 14, 15, 16, 17):  # added 12 to closed list after confirmation from experian team
        acct_status = 'CLOSED'
    elif acct_status in (00, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
                         43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
                         57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                         72, 73, 74, 75, 76, 77, 79, 81, 85, 86, 87, 88, 90, 91,
                         93, 97):
        acct_status = 'SF/WD/WO/SETTLED'
    else:
        acct_status = ''

    
    return  acct_status == 'ACTIVE' # returns bool 