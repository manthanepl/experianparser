from datetime import datetime

from mapping.gender import gender_mapping
from utils.anyHL_LAP_active import checkFor_HL_LAP_active
from utils.anyUL_GL_last12m import checkULorGL_last12m
from utils.anyWrittenOffLast24m import checkWriteOffStatus
from utils.bureauVintageMonths import bureauVintageMonths
from utils.enquiries_last6m import count_enquiries_in_last_six_months
from utils.unsecured_enq_last6m import count_unsec_enq_last6m
from utils.unsecured_loan_before import checkUnsecuredLoans
from utils.writtenOff_accountHolder import totalWrittenOffAmount


def bureauPersonDetails(bureau_data):
    
    if 'added_data' in bureau_data:
        added_data = bureau_data['added_data']
        application_id = added_data['application_id']
        bureau_source = added_data['bureau_source']
        row_id = added_data['row_id']

    if 'INProfileResponse' in bureau_data:
        # print("True")

        applicant_details =  bureau_data['INProfileResponse']['Current_Application']['Current_Application_Details']['Current_Applicant_Details']
        full_name =  applicant_details['First_Name']+' '+applicant_details['Last_Name']
        dob= datetime.strptime(applicant_details['Date_Of_Birth_Applicant'], "%Y%m%d")
        current_date = datetime.now()
        age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
        gender = gender_mapping(applicant_details['Gender_Code'])
        pan = applicant_details['IncomeTaxPan']
        voter_id = applicant_details['Voter_s_Identity_Card']
        drivers_id = applicant_details['Driver_License_Number']
        uid = applicant_details['Universal_ID_Number']
        passport_id = applicant_details['Passport_number']
        ration_id = applicant_details['Passport_number']
        created_datetime = current_date

        if 'SCORE' in bureau_data['INProfileResponse']:
            bureau_score =bureau_data['INProfileResponse']['SCORE']['BureauScore']
            if isinstance(bureau_score,dict): 
                bureau_score = ''
        else:
            bureau_score = ''

        if 'Header' in bureau_data['INProfileResponse']:
            score_date = datetime.strptime(bureau_data['INProfileResponse']['Header']['ReportDate'], "%Y%m%d")
        else:
            score_date =''
        
        # any_unsecured_loan_before 
        CAIS_Account_DETAILS = bureau_data['INProfileResponse']['CAIS_Account']['CAIS_Account_DETAILS']
        any_unsecured_loan_before = checkUnsecuredLoans(CAIS_Account_DETAILS) # returns True if exists else false
        enquiries = bureau_data['INProfileResponse']['CAPS']
        enq_calculation_datetime = current_date
        parsed_date = current_date
        enquiry_6months = count_enquiries_in_last_six_months(enquiries)  # returns count
        enquiry_6months_unsecured = count_unsec_enq_last6m(enquiries) # count
        any_written_off_in_last_24months = checkWriteOffStatus(CAIS_Account_DETAILS) # boolean
        written_off_total_amount ,written_off_principal_amount =  totalWrittenOffAmount(CAIS_Account_DETAILS)
        any_hl_lap_running = checkFor_HL_LAP_active(CAIS_Account_DETAILS) 
        usl_gl_in_last_12months = checkULorGL_last12m(CAIS_Account_DETAILS)
        bureau_vintage_in_months = bureauVintageMonths(CAIS_Account_DETAILS)
        bureau_calculation_datetime = current_date
        max_dpd_in6months = None
        other_dpds_in_last_2years =None
        gl_cc_kcc_el_dpd_in_last_year  = None 
        max_dpd_in_one_year = None

        # print(application_id)
        # print(full_name)
        # print(pan)
        # print("any unsecured loan before",any_unsecured_loan_before)
        # print("Enquiries in last 6 months",enquiry_6months)
        # print("Unsecured Enquiries in last 6 months",enquiry_6months_unsecured)
        # print("Any Written off In last 24 months",any_written_off_in_last_24months)
        # print("Sum of Written off total",written_off_total_amount)
        # print("Sum of written off principal",written_off_principal_amount)
        # print("Any HL / LAP running",any_hl_lap_running)
        # print("Any Unsecured loan or Gold Loan in Last 12 months",usl_gl_in_last_12months)
        # print("Bureau Vintage in Months",bureau_vintage_in_months)
        # print("Bureau Calculation datetime",bureau_calculation_datetime)
        # print("====")

    person_details = {
        "name": full_name, 
        "date_of_birth":dob, 
        "age": age, 
        "gender":gender, 
        "bureau_score":bureau_score, 
        "score_date":score_date, 
        "pan":pan, 
        "voter_id":voter_id,
        "drivers_id":drivers_id, 
        "uid":uid, 
        "enquiry_6months":enquiry_6months, 
        "enq_calculation_datetime":enq_calculation_datetime, 
        "any_unsecured_loan_before":any_unsecured_loan_before, 
        "created_datetime":created_datetime, 
        "passport_id":passport_id, 
        "ration_id":ration_id, 
        "application_id":application_id, 
        "enquiry_6months_unsecured":enquiry_6months_unsecured, 
        "any_written_off_in_last_24months":any_written_off_in_last_24months, 
        "written_off_principal_amount":written_off_principal_amount, 
        "written_off_total_amount": written_off_total_amount, 
        "parsed_date":parsed_date, 
        "any_hl_lap_running":any_hl_lap_running, 
        "usl_gl_in_last_12months":usl_gl_in_last_12months, 
        "bureau_vintage_in_months":bureau_vintage_in_months, 
        "bureau_calculation_datetime":bureau_calculation_datetime,
        "bureau_source":bureau_source,
        "max_dpd_in6months" : max_dpd_in6months,
        "other_dpds_in_last_2years" :other_dpds_in_last_2years,
        "gl_cc_kcc_el_dpd_in_last_year"  :gl_cc_kcc_el_dpd_in_last_year, 
        "max_dpd_in_one_year" : max_dpd_in_one_year
    }

    return person_details