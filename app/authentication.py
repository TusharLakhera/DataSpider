from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def authenticate(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")