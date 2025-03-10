from fastapi import Query, Depends
from utility import email_validator_helper_func, generic_json_response, JWTAuthentication
from .constants import ResponseConstants, RedisConstants
from database import session_dep, get_redis_client
from .models import User
from .utilities import send_otp_helper_func
from gobal_variables import BY_PASS_OTP
from sqlalchemy.future import select


class Login:
    '''
        Api collection to login the user
    '''
    async def post(self, db: session_dep, redis = Depends(get_redis_client), email: str = Query(), otp: str = Query()):
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
            
            
            user_otp, user_details = await redis.mget(RedisConstants.USER_OTP_EMAIL__+email,
                                        RedisConstants.USER_DETAIL_EMAIL__+email)
            
            
            if not user_otp or otp != BY_PASS_OTP:
                return generic_json_response(
                    success = False,
                    status_code = 400,
                    message = ResponseConstants.OTP_IS_INVALID
                )
            
            
            jwt_auth = JWTAuthentication()
            
            if user_details:
                # provide the JWT tokens
                access_token = await jwt_auth.create_access_token(user_details)
                refresh_token = await jwt_auth.create_refresh_token(user_details)
                
                return generic_json_response(
                    success = True,
                    status_code = 200,
                    message = ResponseConstants.USER_LOGIN_SUCCESSFULL,
                    response = {
                        "access_token" : access_token,
                        "refresh_token": refresh_token
                    }
                )

            # finding email in db
            user_details = await db.execute(select(User).filter(User.email == email))
            user_details = user_details.scalars().first()
            
            
            if user_details:
                data = {
                    "id": user_details.id,
                    "email": user_details.email,
                }
                # provide the JWT tokens
                access_token = await jwt_auth.create_access_token(data)
                refresh_token = await jwt_auth.create_refresh_token(data)
                return generic_json_response(
                    success = True,
                    status_code = 200,
                    message = ResponseConstants.USER_LOGIN_SUCCESSFULL,
                    response = {
                        "access_token" : access_token,
                        "refresh_token": refresh_token
                    }
                )
            

            new_user = User(email=email)
            await db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            # provide tokens
            data = {
                "id": new_user.id,
                "email": new_user.email
            }
            
            access_token = await jwt_auth.create_access_token(data)
            refresh_token = await jwt_auth.create_refresh_token(data)
            return generic_json_response(
                success = True,
                status_code = 200,
                message = ResponseConstants.USER_SIGNUP_SUCCESSFULL,
            )
            
        
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