from enum import Enum
from questionary import form
from fastapi_app_manage.enums import PackageManager, Database, DataBaseFramework
import questionary
import tomllib
import tomli_w
import pathlib
import typer
from fastapi_app_manage.write import write_router, write_schema, write_lifespan, write_main, write_settings, \
    write_model, write_database, write_service
from fastapi_app_manage.get_package_version import get_package_versions


def get_package(flag: dict):
    versions = {}
    dependencies = [
        "fastapi", "uvicorn", "pydantic_settings"
    ]
    if flag.get("utils"):
        dependencies.append(
            "fastapi-utils"
        )
    if flag.get("db_framework").title() != "None":
        dependencies.append(
            flag.get("db_framework")
        )
        dependencies.append(
            "asyncmy" if flag.get("database") == "MySQL" else "asyncpg"
        )

    try:
        import fastapi
        versions["fastapi"] = fastapi.__version__
        dependencies.remove("fastapi")
    except ImportError:
        pass
    try:
        import uvicorn
        versions["uvicorn"] = uvicorn.__version__
        dependencies.remove("uvicorn")
    except ImportError:
        pass

    versions = {
        **versions,
        **get_package_versions(dependencies)
    }
    return versions


def generate_dir(
        name: str,
        flag: dict
):
    app_path = pathlib.Path("app")

    app_path.mkdir(exist_ok=True)

    # 创建嵌套文件夹
    router_path = app_path / "router"
    service_path = app_path / "service"
    schema_path = app_path / "schema"
    utils_path = app_path / "utils"
    core_path = app_path / "core"

    router_path.mkdir(exist_ok=True)
    service_path.mkdir(exist_ok=True)
    schema_path.mkdir(exist_ok=True)
    utils_path.mkdir(exist_ok=True)
    core_path.mkdir(exist_ok=True)

    # 创建 __init__.py 文件
    (app_path / "__init__.py").touch()
    (router_path / "__init__.py").touch()
    (service_path / "__init__.py").touch()
    (schema_path / "__init__.py").touch()
    (utils_path / "__init__.py").touch()
    (core_path / "__init__.py").touch()

    if not flag.get("db_framework").title() == "None":
        model_path = app_path / "models"
        model_path.mkdir(exist_ok=True)
        (model_path / "__init__.py").touch()
        (model_path / f"{name}.py").write_text(write_model(flag.get("db_framework")))
        (core_path / f"lifespan.py").write_text(write_lifespan(flag.get("db_framework")))
        if flag.get("db_framework") == "sqlmodel":
            db_engine = core_path / "database.py"
            db_engine.write_text(write_database())

    (router_path / f"{name}.py").write_text(write_router(name, flag.get("utils")))
    (service_path / f"{name}.py").write_text(write_service())
    (schema_path / f"{name}.py").write_text(write_schema())
    if not (core_path / "lifespan.py").exists():
        (core_path / "lifespan.py").write_text(write_lifespan(""))

    with open("main.py", "w") as f:
        f.write(
            write_main(flag.get("cors"))
        )
    with open("settings.py", "w") as f:
        f.write(
            write_settings(flag.get("utils"), flag.get("db_framework"))
        )

    with open(".env", "w") as f:
        f.write(
            """
#env
            """
        )
    versions = get_package(flag)
    if flag.get("packaging") == "pip":
        writes = []
        for pak, ver in versions.items():
            writes.append(
                f"{pak}=={ver}\n"
            )
        with open("requirements.txt", "w") as f:
            f.write("".join(writes))
        typer.echo(f"success create app {name},please install dependenices with pip installl -r requirements.txt")

    else:
        versions = get_package(flag)

        with open("pyproject.toml", "r") as f:
            result = tomllib.loads(f.read())

        result["tool"]["poetry"]["dependencies"].update({
            pak: "^" + version for pak, version in versions.items()
        })
        with open("pyproject.toml", "wb") as f:
            tomli_w.dump(result, f)
        typer.echo(f"success create app {name},please intsall dependencies with poetry install")


def generate_file(
        name: str,
        flag: dict
):
    app_path = pathlib.Path("app")

    router_path = app_path / "router"
    service_path = app_path / "service"
    schema_path = app_path / "schema"

    if not flag.get("db_framework").title() == "None":
        model_path = app_path / "models"
        (model_path / f"{name}.py").write_text(write_model(flag.get("db_framework")))

    (router_path / f"{name}.py").write_text(write_router(name, flag.get("utils")))
    (service_path / f"{name}.py").write_text(write_service())
    (schema_path / f"{name}.py").write_text(write_schema())


def startapp(app_name: str):
    try:
        with open("fastapi-app-manage.toml", "r") as f:
            result = tomllib.loads(f.read())
        generate_file(app_name, result)

    except FileNotFoundError:
        result = form(
            packaging=question(PackageManager),
            db_framework=question(DataBaseFramework)
        ).ask()
        if result.get("db_framework").title() == "None":
            result.update(
                form(
                    utils=binary_question("utils"),
                    cors=binary_question("cors")
                ).ask()
            )
        else:
            result.update(
                form(
                    database=question(Database),
                    utils=binary_question("utils"),
                    cors=binary_question("cors")
                ).ask()
            )
        with open("fastapi-app-manage.toml", "wb") as f:
            tomli_w.dump(result, f)

        generate_dir(app_name, result)


def question(choices: type(Enum)) -> questionary.Question:
    return questionary.select(f"Select the {choices.__name__.lower()}: ", choices=[
        choice.value for choice in list(choices)
    ])


def binary_question(option: str) -> questionary.Question:
    if option == "utils":
        option = "fastapi-utils"

    return questionary.confirm(f"Do you want to add {option}?", default=False)
