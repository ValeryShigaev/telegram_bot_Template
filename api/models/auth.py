from pydantic import BaseModel

from typing import List, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True
        from_attributes = True


class UsersList(BaseModel):
    data: List[User]
    class Config:
        orm_mode = True
        from_attributes = True