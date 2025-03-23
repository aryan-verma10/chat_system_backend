from fastapi import Query, Depends
from utility import email_validator_helper_func, generic_json_response, jwt_auth
from .constants import ResponseConstants, RedisConstants
from database import session_dep, get_redis_client
from .models import User
from .utilities import send_otp_helper_func
from gobal_variables import BY_PASS_OTP
from sqlalchemy.future import select
import json
from .schema import User as user_request_body


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
            
            
            user_otp, user_details = await redis.mget(RedisConstants.USER_OTP_EMAIL+email,
                                        RedisConstants.USER_DETAIL_EMAIL+email)
            
            
            if not user_otp or otp != BY_PASS_OTP:
                return generic_json_response(
                    success = False,
                    status_code = 400,
                    message = ResponseConstants.OTP_IS_INVALID
                )
            
            
            if user_details:
                # provide the JWT tokens
                data = {
                    "id": str(user_details.id),
                    "email": user_details.email
                }
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

            # finding email in db
            user_details = await db.execute(select(User).filter(User.email == email))
            user_details = user_details.scalars().first()
            
            
            if user_details:
                data = {
                    "id": str(user_details.id),
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
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            
            # provide tokens
            data = {
                "id": str(new_user.id),
                "email": new_user.email
            }
            
            access_token = await jwt_auth.create_access_token(data)
            refresh_token = await jwt_auth.create_refresh_token(data)
            return generic_json_response(
                success = True,
                status_code = 200,
                message = ResponseConstants.USER_SIGNUP_SUCCESSFULL,
                response = {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
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
            await redis.set(RedisConstants.USER_OTP_EMAIL+email, otp, ex=300)
            
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



class UserProfile:
    '''
        API collection related to user profile    
    ''' 
    
    async def get(self, db: session_dep, user_id = Depends(jwt_auth.validate_bearer_token), redis = Depends(get_redis_client)):
        '''
             Get api to get the User profile data
        '''
        try:
            cached_profile_details = await redis.get(RedisConstants.USER_PROFILE_DETAILS+user_id)

            if cached_profile_details:
                json_data = json.loads(cached_profile_details)
            
                return generic_json_response(success = True,
                                             status_code = 200,
                                             message = ResponseConstants.USER_PROFILE_DATA_FETCHED_SUCCESSFULLY,
                                             response = json_data)


            user_data = await db.execute(select(User).filter(User.id == user_id))
            user_data = user_data.scalar_one_or_none()
            
            if not user_data:
                return generic_json_response(
                    success = False,
                    status_code = 404,
                    message = ResponseConstants.USER_DATA_NOT_FOUND,
                )
            

            response_body = {
                "id": str(user_data.id),
                "name": user_data.name,
                "user_name": user_data.user_name,
                "email": user_data.email,
                "phone_number": user_data.phone_number
            }

            # caching in redis
            await redis.set(RedisConstants.USER_PROFILE_DETAILS+user_id, json.dumps(response_body), ex=3600) 
            
            return generic_json_response(
                success = True,
                status_code = 200,
                message = ResponseConstants.USER_PROFILE_DATA_FETCHED_SUCCESSFULLY,
                response = response_body
            )
        
        except Exception as err:
            return generic_json_response(
                success = True,
                status_code = 500,
                message = ResponseConstants.INTERNAL_SERVER_ERROR,
                error = str(err)
            )

    
    async def put(self, db: session_dep, request_body : user_request_body, user_id = Depends(jwt_auth.validate_bearer_token), redis = Depends(get_redis_client)):
        try:
            request_body = request_body.model_dump(exclude_none=True)
            if not request_body:
                return generic_json_response(
                    success = True,
                    status_code = 200,
                    message = ResponseConstants.NO_NEW_DATA_UPDATED
                )
            
            user = await db.execute(select(User).filter(User.id == user_id))
            user = user.scalar_one_or_none()
            
            for key, value in request_body.items():
                setattr(user, key, value)

            await db.commit()
            await db.refresh(user)

            # delete outdated information from cache
            await redis.delete(RedisConstants.USER_PROFILE_DETAILS+user_id)

            return generic_json_response(
                success = True,
                status_code = 200,
                message = ResponseConstants.USER_INFO_UPDATED_SUCCESSFULLY
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
user_profile_view = UserProfile()