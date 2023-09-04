def product_class(account_type):
    """
    mapping the account types with respective product account type category 
    """
    # product_classification (Secured/Unsecured)
    if account_type in ('47', '58', '195', '168', '220', '173', '221', '175', '222','33', '172', '219', '184', '185', '191', '223'):
        product_classification = 'Secured'
    else:
        product_classification = 'Unsecured'
        
    # product_classification (Regular Secured and Regular Unsecured)
    if account_type in ('47', '58', '142', '168','31', '173', '221'):
        product_classification = 'Regular Secured'
    elif account_type in ('5', '123', '130', '169', '170', '189', '196', '213', '37', '999'):
        product_classification = 'Regular UnSecured'
        
    # product_classification (Regular/Agri/Commercial)
    if account_type in ('5', '47', '58', '123', '130', '168', '169', '170', '173', '189', '196', '213', '220', '221', '225' , '32', '37' ,'42'): #32 -> 221 , 37 -> 225
        product_classification = 'Regular'
    elif account_type in ('167', '177', '178', '179', '198', '199', '200', '223', '224','226','227', '38', '39'):
        product_classification = 'Agri_PSL'
    elif account_type in ('999', ''):
        product_classification = 'Other & Missing'
    else:
        product_classification = 'Commercial'
        
    # Commercial product_classification (Secured/Unsecured)
    if account_type in ('172', '175', '184', '185', '191', '195', '219', '223', '224'):
        product_classification = 'Commercial Secured'
    elif account_type in ('121', '167', '176', '177', '178', '179', '181', '9', '197', '198', '199', '200', '214','228', '61'):
        product_classification = 'Commercial Unsecured'

    return product_classification
