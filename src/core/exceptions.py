from fastapi import HTTPException, status

def credentials_exception(reason: str = "Could not validate credentials") -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail=reason) 

user_exists_exception: HTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"
)

code_verification_exception: HTTPException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Wrong code"
)

email_not_in_the_system_exception: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Email is not verified"
)

user_not_found: HTTPException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="User not found"
)

def forbidden_wallet_action(reason: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                         detail=reason)