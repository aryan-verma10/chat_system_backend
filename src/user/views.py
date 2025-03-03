from fastapi import Query
from utilities import email_validator_helper_func, generic_json_response
from .constants import ResponseConstants
from database import session_dep
from .models import User

class Login:
    '''
        Api collection to login the user
    '''
    async def post(self, db: session_dep, email: str = Query()):
        '''
            Post api to send otp on the email provided
        '''
        try:
            if not email_validator_helper_func(email):
                return generic_json_response(
                    success = False,
                    status_code = 400,
                    message = ResponseConstants.INVALID_EMAIL
                )
            
            result = db.query(User).filter(User.email == email).all()
            
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


login_view = Login()