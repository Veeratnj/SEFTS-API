from app.schemas.schema import CommonResponse
from fastapi import APIRouter, HTTPException ,Depends
from pydantic import BaseModel
from app.services.login_services import authenticate_user
from app.cryptography.crypt import decrypt
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    encrypted_data: str
    email: str
    password: str

@router.post("/")
async def login(request: LoginRequest,db: Session = Depends(get_db)):
    try:
        # Decrypt the incoming encrypted data
        # decrypted_data = decrypt(request.encrypted_data)
        # print(decrypted_data)
        
        # Parse the decrypted data
        # credentials = eval(decrypted_data)  # Use `json.loads` if the data is in JSON format
        # email = credentials.get("email")
        # password = credentials.get("password")
        
        # Authenticate the user
        data = authenticate_user(email=request.email, password=request.password,db=db)
        print(data)
        # print(token)
        if  data is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return  CommonResponse(
            status=200,
            data=data,
            msg="Login successful"
        )
    except Exception as e:
        print("Error during login:", str(e))
        return  CommonResponse(
            status=401,
            data=[],
            msg="Login failed"
        )