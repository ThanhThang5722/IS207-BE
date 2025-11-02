from fastapi import Depends, HTTPException, status
from app.core.security import decode_token

def role_required(role_name: str):
    def wrapper(token: str = Depends(decode_token)):
        if token.get("role") != role_name:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return token
    return wrapper
