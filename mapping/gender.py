def gender_mapping(gender_code):
    if gender_code == '1':
        gender = 'Male'
    elif gender_code == '2':
        gender = 'Female'
    elif gender_code =='3':
        gender = 'Transgender'
    else:
        gender = 'Unknown'
    return gender

