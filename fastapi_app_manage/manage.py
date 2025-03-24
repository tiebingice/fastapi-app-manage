from enum import Enum
from questionary import form
from .enums import PackageManager, Database, DataBaseFramework
import pathlib
from .write import (
    write_router,
    write_schema,
    write_lifespan,
    write_main,
    write_settings,
    write_model,
    write_database,
    write_service,
    write_router_init_,
    write_router_init,
    write_result,
    write_html,
    write_base_tortoise_model_py,
    write_gitignore,
)
from .utils.get_package import get_package
from .utils.typedict import UserSelectResult
from .utils.format import format_directory_with_black
from typing import cast
import typer
import tomllib
import tomlkit
import questionary


def generate_dir(name: str, flag: UserSelectResult):
    app_path = pathlib.Path("app")

    app_path.mkdir(exist_ok=True)

    # Create nested folders
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

    # Create __init__.py files
    (app_path / "__init__.py").touch()
    (router_path / "__init__.py").touch()
    (service_path / "__init__.py").touch()
    (schema_path / "__init__.py").touch()
    (utils_path / "__init__.py").touch()
    (core_path / "__init__.py").touch()

    if (
        flag.get("db_framework").title() != "None"
    ):  # if db_framework is not None,should create models folder
        model_path = app_path / "models"
        model_path.mkdir(exist_ok=True)
        (model_path / "__init__.py").touch()
        (model_path / f"{name}.py").write_text(write_model(flag.get("db_framework")))

        (core_path / "lifespan.py").write_text(write_lifespan(flag.get("db_framework")))

        if flag.get("db_framework") == "sqlmodel":
            db_engine = core_path / "database.py"
            db_engine.write_text(write_database())

        if flag.get("db_framework") == "tortoise-orm":
            (model_path / "base.py").write_text(write_base_tortoise_model_py())

    (router_path / f"{name}.py").write_text(write_router(name, flag.get("utils")))
    (router_path / "__init__.py").write_text(write_router_init(name))
    (service_path / f"{name}.py").write_text(write_service(name))
    (schema_path / f"{name}.py").write_text(write_schema())
    if not (core_path / "lifespan.py").exists():
        (core_path / "lifespan.py").write_text(write_lifespan(""))

    if flag.get("jinja"):
        templates = app_path / "templates"
        (app_path / "templates").mkdir(exist_ok=True)
        (templates / "index.html").write_text(write_html())

    if flag.get("standresponse"):
        (core_path / "result.py").write_text(write_result())

    if flag.get("git"):
        write_gitignore(flag.get("packaging"))

    with open("main.py", "w") as f:
        f.write(write_main(flag.get("cors"), flag.get("standardfastapi")))

    with open("settings.py", "w") as f:
        f.write(write_settings(flag.get("utils"), flag.get("db_framework")))

    with open(".env", "w") as f:
        f.write("# Environment variable record\n")

    dependencies = " ".join(get_package(flag))
    install_command = ""

    if flag.get("packaging") == "pip":
        install_command = f"pip install {dependencies} "
    elif flag.get("packaging") == "poetry":
        install_command = f"poetry add {dependencies}"
    elif flag.get("packaging") == "uv":
        install_command = f"uv add {dependencies}"

    typer.echo(
        f"Successfully created app '{name}'. Important: Please install dependencies using the following command:"
    )
    typer.echo(f"\n    {install_command}\n", color=True)
    typer.echo("Ensure all dependencies are installed before running the application.")


def generate_file(name: str, flag: UserSelectResult):
    app_path = pathlib.Path("app")

    router_path = app_path / "router"
    service_path = app_path / "service"
    schema_path = app_path / "schema"

    if not flag.get("db_framework").title() == "None":
        model_path = app_path / "models"
        (model_path / f"{name}.py").write_text(write_model(flag.get("db_framework")))

    (router_path / f"{name}.py").write_text(write_router(name, flag.get("utils")))
    code = write_router_init_(name)
    if code:
        (router_path / "__init__.py").write_text(code)
    (service_path / f"{name}.py").write_text(write_service(name))
    (schema_path / f"{name}.py").write_text(write_schema())
    format_directory_with_black()


def startapp(app_name: str):
    try:
        with open("fastapi-app-manage.toml", "r") as f:
            result = tomllib.loads(f.read())

        if app_name in cast(list[str], result.get("apps")):
            typer.echo("Cannot register duplicate app", err=True)
        else:
            generate_file(app_name, cast(UserSelectResult, result))

            result["apps"].append(app_name)
            with open("fastapi-app-manage.toml", "w") as f:
                f.write(tomlkit.dumps(result))

    except FileNotFoundError:
        result = form(
            packaging=question(PackageManager),
            standardfastapi=binary_question("fastapi standard"),
            db_framework=question(DataBaseFramework),
        ).ask()

        if cast(str, result.get("db_framework")).title() == "None":
            result.update(
                form(
                    utils=binary_question("utils"),
                    cors=binary_question("cors"),
                    jinja=binary_question("jinja2 template"),
                    standresponse=binary_question("standard response"),
                    git=binary_question("git"),
                ).ask()
            )
        else:
            result.update(
                form(
                    database=question(Database),
                    utils=binary_question("utils"),
                    cors=binary_question("cors"),
                    jinja=binary_question("jinja2 template"),
                    standresponse=binary_question("standard response"),
                    git=binary_question("git"),
                ).ask()
            )

        result.update({"apps": [app_name]})
        with open("fastapi-app-manage.toml", "w") as f:
            f.write(tomlkit.dumps(result))

        generate_dir(app_name, cast(UserSelectResult, result))


def question(choices: type[Enum]) -> questionary.Question:
    return questionary.select(
        f"Select the {choices.__name__.lower()}: ",
        choices=[choice.value for choice in list(choices)],
    )


def binary_question(option: str) -> questionary.Question:
    if option == "utils":
        option = "fastapi-utils"

    return questionary.confirm(f"Do you want to add {option}?", default=False)
