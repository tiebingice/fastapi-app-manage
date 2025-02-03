
from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    code: int = 200
    msg: str = 'success'
    data: T = None

    @classmethod
    def success(cls, code: int = 200, msg: str = "success", data: T = None) -> T:
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def failure(cls, code: int = 400, msg: str = "failure", data: T = None) -> T:
        return cls(code=code, msg=msg, data=data)

    