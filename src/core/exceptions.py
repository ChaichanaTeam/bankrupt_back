from fastapi import HTTPException, status

credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
)

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