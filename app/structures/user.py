from pydantic import BaseModel, constr


class UserData(BaseModel):
    public_id: str
    username: constr(min_length=8)
    email: str
    password: constr(min_length=8)
    is_admin: bool

    class Config():
        orm_mode = True
