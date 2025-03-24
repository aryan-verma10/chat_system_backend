from pydantic import BaseModel


class User(BaseModel):
    '''
        User request body
    '''
    name: str = None
    user_name: str = None
    phone_number: str = None


class UserConnectionPostSchema(BaseModel):
    '''
        User connection post request body
    '''
    user_connection_id : str 
    user_connection_name: str = None
