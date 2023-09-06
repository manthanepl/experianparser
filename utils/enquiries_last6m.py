
from datetime import datetime,timedelta
def count_enquiries_in_last_six_months(data):

    """
     count the number of credit inquiries made on an individual's credit bureau report within the last six month
    
    """
    # Extract the relevant list of requests
    if "CAPS_Application_Details" in data :
        requests = data.get("CAPS_Application_Details", [])

        # Calculate the date 6 months ago from the current date
        six_months_ago = datetime.now() - timedelta(days=180)

        # Initialize a counter for requests in the last 6 months
        requests_in_last_six_months = 0

        # Iterate through the requests
        for request in requests:
            date_of_request = datetime.strptime(request.get("Date_of_Request", ""), "%Y%m%d")

            # Check if the date of request is within the last 6 months
            if date_of_request >= six_months_ago:
                requests_in_last_six_months += 1

        return requests_in_last_six_months
    
    else:
        return 0