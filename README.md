# FastAPI-APP-Manage

FastAPI-APP-Manage 是一个由Typer构建的命令行工具，能够简化fastapi项目结构的配置。
其作用类似于Django框架中的python manage.py 下的

```
python3 manage.py startapp my_app
```

## 安装方式

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

## 使用方式

### 选择 pip + venv

打开cmd
首先你要创建一个fastapi项目

```
mkdir my_fastapi_project
cd my_fastapi_project
python3 -m venv .venv
```

激活虚拟环境

```
  source .venv/bin/activate # linux/macos
  .venv/Scripts/activate # windows
```

激活后安装本库
安装完毕后，输入指令

```
fastapi-app start my_app
fastapi-app st my_app
```

此时会进行询问,
询问依次是

```
? Select the packagemanager:  pip
? Select the databaseframework:  tortoise-orm
? Select the database:  Postgres
? Do you want to add fastapi-utils? Yes
? Do you want to add cors? Yes
success create app app,please install dependenices with pip installl -r requirements.txt
```

需要注意的是，如果在选择数据库框架的时候选择不使用则不会询问选择数据库
完成后需要安装相关依赖，依赖安装后可以开始编写代码
后续如果要创建新的app，即新的router/service，只需要输入上述指令且无需再进行询问，会自动按照上次配置创建。

### 使用poetry
使用poetry首先你需要按照poetry
然后打开cmd输入
```
poetry new my_fastapi_project
```
创建好poetry项目后，你可以安装本库
```
poetry add fastapi_app_manage --group dev
```
注意这里使用了--group dev意味着这个依赖是一个**开发依赖**，部署的时候不用安装
完成后，输入指令
```
poetry run fastapi-app start my_app
```
或者
```
poetry run fastapi-app st my_app
```
同样会进行询问。
```
? Select the packagemanager:  poetry
? Select the databaseframework:  tortoise-orm
? Select the database:  MySQL
? Do you want to add fastapi-utils? No
? Do you want to add cors? No
success create app app,please intsall dependencies with poetry install

```
询问结束后，安装依赖
```
poetry install
```
依赖完成安装后，可以开始编写代码

与 Django 的 startapp 命令不同，fastapi-app-manage 工具不会将路由、模型类、逻辑、核心部分和工具函数等文件统一放在一个 app 文件夹下。相反，它会将这些文件分别放置在对应的子文件夹中（如 router、models、service、core 等），并用一个 app 文件夹来包含这些子文件夹。
首次使用该指令时，fastapi-app-manage 会自动创建一个 app 文件夹，并在其中添加上述的子文件夹。后续在同一项目中再次执行该指令时，会在已有的子文件夹下继续添加新的文件。