import re
import datetime
import jwt
from fastapi import Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi import HTTPException
from gobal_variables import (JWT_HASHING_ALGORITHM, JWT_SECRET_KEY, 
                              JWT_REFRESH_TOKEN_EXPIRY_MINUTES,
                              JWT_ACCESS_TOKEN_EXPIRY_MINUTES)


def email_validator_helper_func(email: str)->bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(email_regex, email):
        return True
    
    return False

def generic_json_response(success: bool = True, status_code: int = 200, message: str = "", response="", error: str = ""):
    content = {
        "success": success,
        "status_code": status_code,
        "message": message,
        "response": response,
        "error": error
    }

    return JSONResponse(content=content, status_code = status_code)


class JWTAuthentication:
    '''
        JWT Authentication functions
    '''
    REFRESH = "refresh"
    ACCESS = "access"

    def __init__(self):
        self.datetime_format = r"""%Y-%m-%d %H:%M:%S.%f"""
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JWT_HASHING_ALGORITHM
        self.access_token_expiry_min = int(JWT_ACCESS_TOKEN_EXPIRY_MINUTES)
        self.refresh_token_expiry_min = int(JWT_REFRESH_TOKEN_EXPIRY_MINUTES)

    async def create_access_token(self, data: dict)->str:
        '''
            access token creation
        '''     
        to_encode = data.copy()
        expiry = str(datetime.datetime.utcnow()+datetime.timedelta(self.access_token_expiry_min))
        to_encode["expiry"] = expiry
        to_encode["token_type"] = self.ACCESS 

        access_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return access_token
    
    
    async def create_refresh_token(self, data: dict)->str:
        '''
            refresh token generation
        ''' 
        to_encode = data.copy()
        expiry = str(datetime.datetime.utcnow()+datetime.timedelta(self.refresh_token_expiry_min))
        to_encode["expiry"] = expiry
        to_encode["token_type"] = self.REFRESH

        refresh_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return refresh_token


    async def decode_access_token(self, access_token: str)->dict:
        '''
            decode the jwt access token 
        '''
        try:
            
            payload = jwt.decode(access_token, self.secret_key, algorithms=self.algorithm)
            expiry_time = datetime.datetime.strptime(payload["expiry"], self.datetime_format)
            token_type = payload["token_type"]
            
            if datetime.datetime.utcnow()>expiry_time:
                raise Exception("Token expired")

            if token_type != self.ACCESS:
                raise Exception("Invalid token")                   
            
            return payload


        except Exception as err:
            return {"error": err}


    async def decode_refresh_token(self, refresh_token: str)->dict:
        '''
            decode the jwt access token 
        '''
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=self.algorithm)
            expiry_time = datetime.datetime.strptime(payload["expiry"], self.datetime_format)
            token_type = payload["token_type"]
            if datetime.datetime.utcnow()>expiry_time:
                raise Exception("Token expired")

            if token_type != self.REFRESH:
                raise Exception("Invalid token")                   
            
            return payload


        except Exception as err:
            return {"error": err}
        


    async def validate_bearer_token(self, auth: str = Security(HTTPBearer())):
        '''
            Helper function to validate the bearer token
        '''

        token = auth.credentials
        try:
            decoded_data = await self.decode_access_token(access_token=token)
            return decoded_data["id"]

        except Exception as err:
            raise HTTPException(
                status_code=403,
                detail = "Invalid token provided."
            )
        
jwt_auth = JWTAuthentication()