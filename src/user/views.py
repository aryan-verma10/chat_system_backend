from fastapi import Query, Depends
from utility import email_validator_helper_func, generic_json_response
from .constants import ResponseConstants, RedisConstants
from database import session_dep, get_redis_client
from .models import User
from .utilities import send_otp_helper_func


class Login:
    '''
        Api collection to login the user
    '''
    async def post(self, db: session_dep, email: str = Query()):
        '''
            Post api to provide JWT tokens after successfull login
        '''
        try:
            if not email_validator_helper_func(email):
                return generic_json_response(
                    success = False,
                    status_code = 400,
                    message = ResponseConstants.INVALID_EMAIL
                )
            
            
            user_email = await redis.get(f"user_login_email__{email}")
            if user_email:
                # provide tokens 
                return generic_json_response(
                    success = True,
                    status_code = 200,
                    message = ResponseConstants.USER_LOGIN_SUCCESSFULL
                )
            
            # finding email in db
            user_email = await db.query(User).filter(User.email == user_email).first()

            if user_email:
                # provide tokens
                return generic_json_response(
                    success = True,
                    status_code = 200,
                    message = ResponseConstants.USER_LOGIN_SUCCESSFULL,
                )
            
            return {
                "message": "hello world"
            }
        
        except Exception as err:
            return generic_json_response(
                success = False,
                status_code = 500,
                message = ResponseConstants.INTERNAL_SERVER_ERROR,
                error = str(err)
            )
        

class SentOtp:
    '''
        API collection to send otp to the email provided
    '''
    async def post(self, email: str = Query(), redis = Depends(get_redis_client)):
        '''
            Post api to sent otp
        '''
        try:
            if not email_validator_helper_func(email):
                return generic_json_response(
                    success = False,
                    status_code = 400,
                    message = ResponseConstants.INVALID_EMAIL
                )
            
            otp = await send_otp_helper_func(email)
            await redis.set(RedisConstants.USER_OTP_EMAIL__+email, otp, ex=300)
            
            return generic_json_response(
                success = True,
                status_code = 200,
                message = ResponseConstants.OTP_SENT_SUCCESSFULLY,
            )
        

        except Exception as err:
            return generic_json_response(
                success = False,
                status_code = 500,
                message = ResponseConstants.INTERNAL_SERVER_ERROR,
                error = str(err)
            )


login_view = Login()
sent_otp_view = SentOtp()