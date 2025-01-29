from typing import TypedDict,NotRequired

class UserSelectResult(TypedDict):
    packaging:str
    standardfastapi:bool
    db_framework:str
    utils:bool
    cors:bool
    jinja:bool
    standresponse:bool
    database:NotRequired[str]


