from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
