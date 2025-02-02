
from .typedict import UserSelectResult


def get_package(flag:UserSelectResult)->list[str]:
 
    dependencies = [
        "fastapi", "uvicorn", "pydantic_settings"
    ]

    if flag.get("utils"): #if utils is True,means add fastapi-utils
        dependencies.append(
            "fastapi-utils"
        )
        dependencies.append(
            "typing_inspect"
        )


    if flag.get("db_framework").title() != "None": #if db_framework is not None,means add asyncmy or asyncpg
        dependencies.append(
            flag.get("db_framework")
        )
        dependencies.append(
            "asyncmy" if flag.get("database") == "MySQL" else "asyncpg"
        )
    

    if flag.get("jinja"): #if jinja is True,means add jinja2
        dependencies.append(
            "jinja2"
        )
    
    if flag.get("standardfastapi"):
       dependencies[0]="fastapi[standard]"
       dependencies.append(
            "orjson"
       )
   
  

    return dependencies