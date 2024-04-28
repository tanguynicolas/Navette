from pydantic import EmailStr
from fastapi import HTTPException

import models

def check_user_email(email: EmailStr, user: models.User):
    if not user:
        raise HTTPException(status_code=404, detail=f"User identified by {email} not found")
    return