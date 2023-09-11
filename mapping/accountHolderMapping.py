def map_account_holder_type(code):
    account_holder_types = {
        '1': 'Individual',
        '2': 'Joint',
        '3': 'Authorized User',
        '7': 'Guarantor',
        'Z': 'Deceased',
    }
    return account_holder_types.get(code, 'Unknown')