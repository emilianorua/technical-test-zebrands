from pydantic import BaseModel, constr


class AuthData(BaseModel):
    username: constr(min_length=8)
    password: constr(min_length=8)
