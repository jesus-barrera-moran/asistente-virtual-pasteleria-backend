from pydantic import BaseModel

class LiteUser(BaseModel):
    username: str
    disabled: bool
    id_role: str