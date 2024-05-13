from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

internal_auth_token = "XXXX-YYYY-ZZZZ-AAAA"
auth_token = APIKeyHeader(name="AUTH-TOKEN")

def authenticate(auth_token: str = Depends(auth_token)):
    if auth_token != internal_auth_token:
        raise HTTPException(status_code=401, detail="Invalid API key")