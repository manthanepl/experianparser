def map_suit_filed_status(code):
    code = int(code)  # Convert the input code to an integer
    suit_filed_statuses = {
        0: 'No Suit Filed',
        1: 'Suit Filed',
        2: 'Wilful Default',
        3: 'Suit Filed (Wilful Default)',
    }
    return suit_filed_statuses.get(code, 'Unknown')