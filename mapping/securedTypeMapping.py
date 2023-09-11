def isSecured(account_type):
    """
    mapping the account types with respective product account type category 
    """
    if account_type in ('47', '58', '195', '168', '220', '173', '221', '175', '222','33', '172', '219', '184', '185', '191', '223'):
        type = 'Secured'
        return True
    else:
        type = 'Unsecured'
        return False 