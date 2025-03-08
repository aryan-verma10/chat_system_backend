import re
from fastapi.responses import JSONResponse


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

