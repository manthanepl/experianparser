from datetime import datetime, timedelta
from utils.unsecured_loan_before import SecuredOrUnsecuredLoan


def count_unsec_enq_last6m(data):

    """
    Counting unsecured loan inquiries made in the last 6 month
    """
    # Extract the relevant list of requests
    if "CAPS_Application_Details" in data:
        requests = data.get("CAPS_Application_Details", [])

        # Calculate the date 6 months ago from the current date
        six_months_ago = datetime.now() - timedelta(days=180)

        # Initialize a counter for requests that match the specified enquiry reason
        num_unsec_enq = 0

        # Iterate through the requests
        for request in requests:
            date_of_request = datetime.strptime(request.get("Date_of_Request", ""), "%Y%m%d")
            reason = request.get("Enquiry_Reason", "")

            # Check if the date of request is within the last 6 months and the reason matches
            if date_of_request >= six_months_ago and SecuredOrUnsecuredLoan(reason) == 'Unsecured':
                num_unsec_enq += 1

        return num_unsec_enq
    else:
        return 0
