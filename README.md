# FastAPI-APP-Manage

FastAPI-APP-Manage 是一个由Typer构建的命令行工具，能够简化fastapi项目结构的配置。使得开发者能够快速创建一个FastAPI应用。本第三方工具通过编写常用的配置代码使得开发者可以快速创建一个FastAPI应用。
创建该第三方库的最初灵感来自于Django框架中的python manage.py 下的

```
python3 manage.py startapp my_app
```

**该第三方库同时也创建了项目的main.py和settings.py两个重要文件，进一步帮助开发者快速开发。**

## 安装方式（注意该工具需要python版本>=3.11)

你可以下载安装用如下指令：

```
pip install fastapi_app_manage
```

或者使用poetry

```
poetry add fastapi_app_manage --group dev
```

实际上该库会安装typer,black等常用的开发依赖，因此使用poetry安装的时候可以使用开发依赖的方式安装，这样做的好处是使得这些库只存在本地开发中，在生产环境中不存在。
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
fastapi-app st my_app （简写）
```

此时会进行询问,
询问依次是

```markdown
? Select the packagemanager:  pip #包管理器，这里选择pip，支持pip和poetry
? Do you want to add fastapi standard? Yes #是否启用安装fastapi[standard],即能够安装fastapi开发中的其余的常用依赖例如文件上传的python-mutipart
? Select the databaseframework:  tortoise-orm #数据库框架，目前仅支持sqlmodel和tortoise-orm
? Select the database:  PostgresSQL #数据库，目前支持MySQL和PostgressSQL
? Do you want to add fastapi-utils? Yes #fastapi-utils第三方插件，用于帮助fastapi开发，引入后将使用类试图和APISettings
? Do you want to add cors? Yes #跨域
? Do you want to add jinja2 template? Yes #模板引擎，目前支持jinja2
? Do you want to add standard response? Yes #标准响应
```

需要注意的是，如果在选择数据库框架的时候选择不使用则不会询问选择数据库
完成后需要安装相关依赖，依赖安装后可以开始编写代码
后续如果要创建新的app，即新的router/service，只需要输入上述指令且无需再进行询问，会自动按照上次配置创建。
同时因为很多时候每个app对应的路由router彼此之前可能会存在嵌套关系（例如下方例子），因此本指令并不会将router进行include_router函数操作，故需要开发者自行编写代码完成。

```python
from fastapi import APIRouter
from .user import user_router as user
from .login import login_router as login

router = APIRouter()
user.include_router(login, prefix="/users/logins")
router.include_router(user)

```

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

```markdown
? Select the packagemanager:  poetry #包管理器，这里使用poetry，支持pip和poetry
? Do you want to add fastapi standard? Yes #是否启用安装fastapi[standard],即能够安装fastapi开发中的其余的常用依赖例如文件上传的python-mutipart
? Select the databaseframework:  tortoise-orm #数据库框架，目前仅支持sqlmodel和tortoise-orm
? Select the database:  MySQL #数据库，目前支持MySQL和PostgressSQL
? Do you want to add fastapi-utils? Yes #fastapi-utils第三方插件，用于帮助fastapi开发，引入后将使用类试图和APISettings
? Do you want to add cors? Yes #跨域
? Do you want to add jinja2 template? Yes #模板引擎，目前支持jinja2
? Do you want to add standard response? Yes #标准响应
```

询问结束后，安装依赖

```
poetry install
```

依赖完成安装后，可以开始编写代码

与 Django 的 startapp 命令不同，fastapi-app-manage 工具不会将路由、模型类、逻辑、核心部分和工具函数等文件统一放在一个 app
文件夹下。相反，它会将这些文件分别放置在对应的子文件夹中（如 router、models、service、core 等），并用一个 app 文件夹来包含这些子文件夹。
首次使用该指令时，fastapi-app-manage 会自动创建一个 app 文件夹，并在其中添加上述的子文件夹。后续在同一项目中再次执行该指令时，会在已有的子文件夹下继续添加新的文件。

## 未来计划

引入更多的可选的配置，例如引入Redis数据库配置、引入MongoDB数据库配置、开发常用工具类等。
