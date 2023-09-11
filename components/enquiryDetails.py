from datetime import datetime

from mapping.loanTypeMapping import loanTypeMapping
from utils.unsecured_loan_before import SecuredOrUnsecuredLoan


def enquiryDetails(bureau_data,account_holder_id,person_details):
    

    if 'INProfileResponse' in bureau_data:
        enquiries = bureau_data['INProfileResponse']['CAPS']
        if 'CAPS_Application_Details' in enquiries:
            enquiry_details = enquiries['CAPS_Application_Details']

            if isinstance(enquiry_details,list):
                for enquiry in enquiry_details:
                    enquiry_date = datetime.strptime(enquiry.get("Date_of_Request", ""), "%Y%m%d")
                    memberShortName = person_details['name']
                    enquiryAmount = int(enquiry['Amount_Financed']) if enquiry['Amount_Financed'] !='' else 0
                    enquiryPurpose =  loanTypeMapping(int(enquiry['Enquiry_Reason'])) if enquiry['Enquiry_Reason'] !='' else ''
                    index = None
                    secured =  SecuredOrUnsecuredLoan(enquiry.get('Enquiry_Reason','')) == 'Secured' 

            
                enquiry_details = {
                    'member_short_name' : memberShortName,
                    'enquiry_purpose' : enquiryPurpose,
                    'enquiry_amount' : enquiryAmount,
                    'enquiry_date':enquiry_date,
                    'index': '',
                    'account_holder_id':account_holder_id,
                    'secured':secured
                }

            else :
                    enquiry_date = datetime.strptime(enquiry_details.get("Date_of_Request", ""), "%Y%m%d")
                    memberShortName = person_details['name']
                    enquiryAmount = int(enquiry_details['Amount_Financed']) if enquiry_details['Amount_Financed'] !='' else 0
                    enquiryPurpose =  loanTypeMapping(int(enquiry_details['Enquiry_Reason'])) if enquiry_details['Enquiry_Reason'] !='' else ''
                    index = None
                    secured =  SecuredOrUnsecuredLoan(enquiry_details.get('Enquiry_Reason','')) == 'Secured' 

            
                    enquiry_details = {
                        'member_short_name' : memberShortName,
                        'enquiry_purpose' : enquiryPurpose,
                        'enquiry_amount' : enquiryAmount,
                        'enquiry_date':enquiry_date,
                        'index': '',
                        'account_holder_id':account_holder_id,
                        'secured':secured
                    }
                
        else: 

                    return {
                        'member_short_name' : None,
                        'enquiry_purpose' : None,
                        'enquiry_amount' : 0,
                        'enquiry_date':None,
                        'index': '',
                        'account_holder_id':account_holder_id,
                        'secured':None
                    }
            

        return enquiry_details