import pathlib
import typer
from .code import (
    py_api_router_code,
    py_api_router_cbv_code,
    py_service_code,
    py_schema_code,
    py_lifespan_code,
    index_html,
    py_router_init_code,
    write_base_tortoise_model_py_code,
    py_tortoise_orm_code,
    py_sqlmodel_code,
    py_core_db,
    py_cors_fastapi_code,
    py_pydantic_settings_code,
    py_pydantic_settings_code_,
    py_standard_response_code,
)


def write_gitignore(package: str) -> str:
    gitignore_set = {".venv", ".env", ".env.*", "fastapi-app-manage.toml"}
    gitignore_path = pathlib.Path(".gitignore")
    if package == "poetry":
        gitignore_set.add("poetry.lock")
    elif package == "uv":
        gitignore_set.add("uv.lock")

    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            existing_content = f.read().splitlines()
        for line in existing_content:
            if line.strip():
                gitignore_set.add(line.strip())

    gitignore_path.write_text("\n".join(list(gitignore_set)))

    return "gitignore"


def write_base_tortoise_model_py() -> str:
    return write_base_tortoise_model_py_code


def write_html() -> str:
    return index_html


def write_router(name: str, is_utils: bool = False) -> str:
    if is_utils:
        return py_api_router_cbv_code.format(name.title())
    else:
        return py_api_router_code


def write_service(name: str) -> str:
    return py_service_code.format(name.title())


def write_schema() -> str:
    return py_schema_code


def write_lifespan(db_framwork: str = "tortoise-orm") -> str:
    if db_framwork == "tortoise-orm":
        return py_lifespan_code.replace(
            "#1",
            """async with RegisterTortoise(
        app=app,
        config=settings.tortoise_config
    ): """,
        )
    else:
        return py_lifespan_code.replace("#1", "")


def write_model(db_framwork: str) -> str:
    if db_framwork == "tortoise-orm":
        return py_tortoise_orm_code
    else:
        return py_sqlmodel_code


def write_database() -> str:
    return py_core_db


def write_main(cors: bool = False, standard_: bool = False) -> str:
    if cors and standard_:
        return (
            py_cors_fastapi_code.replace(
                "#1",
                """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           """,
            )
            .replace("#2", "from fastapi.middleware.cors import CORSMiddleware")
            .replace("#3", "default_response_class=ORJSONResponse")
            .replace("#4", "from fastapi.responses import ORJSONResponse")
        )
    elif cors:
        return (
            py_cors_fastapi_code.replace(
                "#1",
                """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           """,
            )
            .replace("#2", "from fastapi.middleware.cors import CORSMiddleware")
            .replace("#3", "")
            .replace("#4", "")
        )
    elif standard_:
        return (
            py_cors_fastapi_code.replace("#3", "default_response_class=ORJSONResponse")
            .replace("#1", "")
            .replace("#2", "")
            .replace("#4", "from fastapi.responses import ORJSONResponse")
        )
    else:
        return (
            py_cors_fastapi_code.replace("#1", "")
            .replace("#2", "")
            .replace("#3", "")
            .replace("#4", "")
        )


def write_settings(utils: bool = False, db_framework: str = "None") -> str:
    code = py_pydantic_settings_code
    if utils:
        code = py_pydantic_settings_code_

    if db_framework.title() == "None":
        return code.replace("#1", "").replace("#2", "")

    elif db_framework == "tortoise-orm":
        return code.replace(
            "#1",
            """@property
    def tortoise_config(self):
        return {
            'connections': {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.mysql', #note: Replace according to the used database version, here we do not directly write the corresponding driver.
                    'credentials': {
                        'host': self.db_host,
                        'port': self.db_port,
                        'user': self.db_user,
                        'password': self.db_password,
                        'database': self.database,
                    }
                },
        
            },
            'apps': {
                'models': {
                    'models': ['app.models'],
                    'default_connection': 'default',
                }
            }
        }

        """,
        ).replace(
            "#2",
            """db_host:str="127.0.0.1"
    db_port:int=6379
    db_user:str="root"
    db_password:str="pwd"
    database:str="db"
            """,
        )
    else:
        return code.replace(
            "#1",
            """@property
    def database_url(self):
        return f"pymysql+mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}" # #note: Replace according to the used database version, here we do not directly write the corresponding driver.
        """,
        ).replace(
            "#2",
            """db_host:str="127.0.0.1"
    db_port:int=6379
    db_user:str="root"
    db_password:str="pwd"
    database:str="db"
            
            """,
        )


def write_router_init(name: str) -> str:
    return py_router_init_code.format(name=name)


def write_router_init_(name: str) -> str:
    app_path = pathlib.Path("app")
    router_path = app_path / "router"
    router_path_init = router_path / "__init__.py"
    try:
        code = router_path_init.read_text()
        index = code.find("from fastapi import APIRouter")
        if index != -1:
            update_index = index + len("from fastapi import APIRouter")
            update_code = (
                code[:update_index]
                + f"\nfrom .{name} import router as {name}_router"
                + code[update_index:]
            )
            return update_code
        typer.echo("Cannot rewrite router __init__.py", err=True)
        return code
    except UnicodeDecodeError:
        typer.echo(
            "Error reading __init__.py. The file may contain non-UTF-8 characters.",
            err=True,
        )
        return ""


def write_result() -> str:
    return py_standard_response_code
