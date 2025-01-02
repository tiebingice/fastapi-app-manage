# FastAPI-APP-Manage

FastAPI-APP-Manage 是一个由Typer构建的命令行工具，能够简化fastapi项目结构的配置。
你可以下载安装用如下指令：

```
pip install fastapi_app_manage
```

或者使用poetry

```
poetry add fastapi_app_manage --group dev
```

完成后你将可以在命令行输入如下指令

```
fastapi-app start [appname]


```

简写方式

```
fastapi-app st [appname]

```

第一次的时候会询问用户配置后续会将配置存入fastapi-app-manage.toml文件下，后续不会再次询问