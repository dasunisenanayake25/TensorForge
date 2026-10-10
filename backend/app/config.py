import os
from fastapi import Request

TEAM_CYLIX_KEY = "tf2_0b0b7dc05ae49ce296bbd0d1fb596980a2b7dba11e4d6e80"
MODEL_VERSION_TAG = "v1.2" # Change this whenever Member 1 updates the model

class UnauthorizedException(Exception):
    pass

async def verify_api_key(request: Request):
    api_key_header = request.headers.get("X-API-Key")
    auth_header = request.headers.get("Authorization")
    
    extracted_key = None
    if api_key_header:
        extracted_key = api_key_header
    elif auth_header and auth_header.startswith("Bearer "):
        extracted_key = auth_header.split(" ")[1]
        
    expected_key = os.getenv("API_KEY", TEAM_CYLIX_KEY)
    
    if not extracted_key or extracted_key != expected_key:
        raise UnauthorizedException()
        
    return extracted_key