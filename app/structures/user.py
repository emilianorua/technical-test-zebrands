import enum
from pydantic import BaseModel, constr


class Roles(str, enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class UserData(BaseModel):
    public_id: str
    username: constr(min_length=8)
    email: str
    password: constr(min_length=8)
    role: Roles

    class Config():
        orm_mode = True
