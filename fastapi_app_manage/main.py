import typer
from fastapi_app_manage.manage import startapp


app = typer.Typer(
    help="FastAPI Project Helpers",
    name="FastAPI APP Manage",
)


@app.command()
def start(app_name: str):
    # 启动一个新的FastAPI应用，应用名称由app_name参数指定
    startapp(app_name)


@app.command()
def st(app_name: str):
    startapp(app_name)


if __name__ == "__main__":
    app()
