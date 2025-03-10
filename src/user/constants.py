class ResponseConstants:
    INVALID_EMAIL = "Invalid Email."
    INTERNAL_SERVER_ERROR = "Internal Server Error."
    OTP_SENT_SUCCESSFULLY = "OTP sent succcessfully."
    USER_LOGIN_SUCCESSFULL = "User login successfull."
    OTP_IS_INVALID = "Otp is invalid."
    USER_SIGNUP_SUCCESSFULL = "User sign-up successfull."


class RedisConstants:
    '''
        cache names for redis
    '''
    USER_OTP_EMAIL__ = "user_otp_email__"
    USER_DETAIL_EMAIL__ = "user_detail_email__"