def map_paymentFrequency(code):
    paymentFrequency_types = {
        'D': 'Deferred',
        'P': 'Single payment loan',
        'W': 'Weekly',
        'B': 'Bi-Weekly',
        'E': 'Semi-monthly',
        'M': 'Monthly',
        'L': '2 monthly (bimonthly)',
        'Q': '3 monthly (quarterly)',
        'T': 'Triannually',
        'S': 'Semiannually',
        'Y': 'Annually',
        'X': 'Variable',
        'U': 'Unknown',
    }
    return paymentFrequency_types.get(code, 'Unknown')