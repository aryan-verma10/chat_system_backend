class ResponseConstants:
    INVALID_EMAIL = "Invalid Email."
    INTERNAL_SERVER_ERROR = "Internal Server Error."
    OTP_SENT_SUCCESSFULLY = "OTP sent succcessfully."
    USER_LOGIN_SUCCESSFULL = "User login successfull."
    OTP_IS_INVALID = "Otp is invalid."
    USER_SIGNUP_SUCCESSFULL = "User sign-up successfull."
    USER_PROFILE_DATA_FETCHED_SUCCESSFULLY = "User profile data fetched successfully."
    USER_DATA_NOT_FOUND = "User data not found."
    NO_NEW_DATA_UPDATED = "No new data updated in user profile."
    USER_INFO_UPDATED_SUCCESSFULLY = "User information updated successfully."

class RedisConstants:
    '''
        cache names for redis
    '''
    USER_OTP_EMAIL = "user_otp_email:"
    USER_DETAIL_EMAIL = "user_detail_email:"
    USER_PROFILE_DETAILS = "user_profile_details:"