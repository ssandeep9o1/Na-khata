import os
# Import HTTPBearer and HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

# Define the new bearer scheme
bearer_scheme = HTTPBearer()

# --- Credentials ---
SECRET_KEY = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
    Decodes the JWT token from the request to get the current user's data.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            audience="authenticated"
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return payload

    except JWTError as e:
        print(f"JWT Validation Error: {e}")
        raise credentials_exception