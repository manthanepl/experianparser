def SecuredOrUnsecuredLoan(account_type):
    if account_type in ('47', '58', '195', '168', '220', '173', '221', '175', '222','33', '172', '219', '184', '185', '191', '223'):
        loan_type = 'Secured'
    else:
        loan_type = 'Unsecured'
    return loan_type

def checkUnsecuredLoans(CAIS_Account_DETAILS):
    """
    Returns True if The customer has any opted  for Unsecured loan in any  previous loans Else returns False
    """

    # if multiple tradelines exists
    if isinstance(CAIS_Account_DETAILS,list):
    
        # calculate number of unsecured loan accounts
        no_of_ul = sum(1 for account in CAIS_Account_DETAILS if SecuredOrUnsecuredLoan(account.get('Account_Type')) == 'Unsecured')

        # no business loan  accounts 
        if no_of_ul == 0:
            return False 
        elif no_of_ul > 0:
            return True
        
    # if it is a single tradeline
    # elif isinstance(CAIS_Account_DETAILS,dict):
    else:
        if SecuredOrUnsecuredLoan(CAIS_Account_DETAILS.get('Account_Type')) == 'Unsecured':
            return True
        else:
            return False
