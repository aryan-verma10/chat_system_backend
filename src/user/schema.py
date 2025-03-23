from pydantic import BaseModel


class User(BaseModel):
    '''
        User request body
    '''
    name: str = None
    user_name: str = None
    phone_number: str = None

