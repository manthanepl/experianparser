from datetime import datetime

current_date = datetime.now()

# Convert current_date to the desired string format
date_string = current_date.strftime("%Y%m%d")

print(date_string)

print(type(date_string))