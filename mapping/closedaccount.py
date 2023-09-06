from datetime import datetime as dt

# calculate the flag if the account is active returns 0 else 1 
# if closed date is mention then account is closed else active.
def closed_account(closed_date):
    closed_acc_date= dt.strptime(closed_date, '%Y%m%d') if closed_date!='' else ''
    closed_flag = 0 if (closed_acc_date !='') else 1
    return closed_flag
