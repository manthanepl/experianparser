

def map_collateral_type(code):
    collateral_types = {
        '99': 'No Collateral ',
        '11': 'Property',
        '12': 'Gold',
        '13': 'Shares',
        '14': 'Saving Account and Fixed Deposit',
    }
    return collateral_types.get(code, None)