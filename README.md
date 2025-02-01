### FastAPI-APP-Manage: 快速构建与管理 FastAPI 应用的利器

**概述**

`FastAPI-APP-Manage` 是一款基于 Typer 构建的命令行工具，旨在简化 FastAPI 项目的初始化和配置。它允许开发者通过简单的命令快速搭建一个结构化的
FastAPI 应用，并提供了一系列预设选项来加速开发流程。此工具的设计灵感来源于 Django 框架中常用的
`python manage.py startapp my_app` 命令，不仅创建了项目的基本文件结构，还自动生成了 `main.py` 和 `settings.py`
文件，以帮助开发者更快地开始编码。

## 安装指导

确保您的 Python 版本不低于 3.11（请注意：0.2.1 版本存在无限递归问题，建议避免使用该版本）。以下是安装方法：

### 使用 pip 安装

```bash
pip install fastapi_app_manage
```

### 使用 Poetry 安装（推荐）

Poetry 是一种用于依赖管理和打包的现代工具，能够更好地隔离开发环境。使用 Poetry 安装 `fastapi_app_manage`
的好处是这些依赖仅存在于本地开发环境中，不会影响生产部署。

```bash
poetry add fastapi_app_manage --group dev
```

安装完成后，您可以使用以下命令启动一个新的 FastAPI 应用程序：

```bash
fastapi-app start [appname]
# 或者简写为:
fastapi-app st [appname]
```

## 创建新应用

### 方法一：使用 pip + venv

#### 步骤 1：创建并进入项目目录

```bash
mkdir my_fastapi_project && cd $_
```

#### 步骤 2：创建虚拟环境并激活

- 对于 Linux/MacOS 用户：

  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  ```

- 对于 Windows 用户：

  ```bash
  python3 -m venv .venv && .venv\Scripts\activate
  ```

#### 步骤 3：安装 `FastAPI-APP-Manage` 并创建应用

运行 `fastapi-app start my_app` 或其简写形式 `fastapi-app st my_app` 来启动新的应用程序创建过程。

### 方法二：使用 Poetry

#### 步骤 1：创建 Poetry 项目

```bash
poetry new my_fastapi_project
```

#### 步骤 2：安装 `FastAPI-APP-Manage`

```bash
poetry add fastapi_app_manage --group dev
```

#### 步骤 3：创建应用

运行 `poetry run fastapi-app start my_app` 或 `poetry run fastapi-app st my_app` 来创建新应用。创建后，根据提示选择配置选项。

## 配置选项说明

在创建应用时，您将被问到一系列问题来定制您的项目配置。每个问题都旨在帮助您根据需要设置最佳实践配置。以下是详细的配置项介绍：

```markdown
? Select the packagemanager:  pip
? Do you want to add fastapi standard? Yes
? Select the databaseframework:  tortoise-orm
? Select the database:  PostgresSQL
? Do you want to add fastapi-utils? Yes
? Do you want to add cors? Yes
? Do you want to add jinja2 template? Yes
? Do you want to add standard response? Yes 
```

以下是对其的介绍

- **包管理器选择 (`Select the packagemanager`)**
    - 提供两个选项：`pip` 和 `poetry`，用于管理项目的依赖关系。

- **是否添加 FastAPI 标准配置 (`Do you want to add fastapi standard?`)**
    - 如果选择“是”，则会安装 FastAPI 及其开发中常用的额外依赖，例如处理文件上传所需的 `python-multipart`，以及其他有助于开发的标准库。

- **数据库框架选择 (`Select the databaseframework`)**
    - 当前支持 `sqlmodel` 和 `tortoise-orm`，这两个 ORM 工具可以帮助定义数据模型并与数据库交互。

- **数据库选择 (`Select the database`)**
    - 支持 MySQL 和 PostgreSQL 数据库，选择合适的数据库类型对于应用性能至关重要。

- **是否添加 `fastapi-utils` 插件 (`Do you want to add fastapi-utils?`)**
    - `fastapi-utils` 是一个第三方插件，提供了诸如类视图、API 设置等功能，可以增强 FastAPI
      的开发体验。选择后将会使用类视图CBV作为路由函数，同时配置类也变为了APISetting

- **是否启用跨域资源共享 (CORS) (`Do you want to add cors?`)**
    - 如果您的应用需要与不同的源进行通信，则应启用 CORS 支持。

- **是否添加 Jinja2 模板引擎 (`Do you want to add jinja2 template?`)**
    - 如果计划使用模板渲染 HTML 页面，则可以选择集成 Jinja2 模板引擎。

- **是否添加标准响应配置 (`Do you want to add standard response?`)**
    - 这将设置默认的响应格式。如果选择了 FastAPI 标准配置，默认的响应类会采用 ORJSON 进行序列化，提供更快的性能。

### 注意事项

- 如果不选择数据库框架，则不会询问关于具体数据库的选择。
- 完成配置后，需要根据所选的包管理器安装相关依赖。
- 后续创建新的 app（即新的路由和服务）只需再次输入上述指令，无需重复配置过程，会自动按照上次配置创建。
- 路由之间的嵌套关系需自行编写代码完成，例如通过 `include_router` 函数操作。
- 选择标准的FastAPI,同时也会使用orjson替代默认的json库做默认响应序列化。
- 选项完成后，会提示安装指令，如果你还没有安装这些依赖请根据自己的选择使用安装指令安装。如果你已经安装了依赖，可以直接开始开发。

## 项目结构

不同于 Django 的集中式 app 文件夹结构，`FastAPI-APP-Manage` 推崇模块化的子文件夹组织方式（如 `router`, `models`,
`service`, `core` 等），使代码更加清晰易读。首次使用该指令时，`FastAPI-APP-Manage` 会自动创建一个 app
文件夹，并在其中添加上述的子文件夹。在同一项目中再次执行该指令时，会在已有的子文件夹下继续添加新的文件。

## 未来计划

未来版本计划增加更多可选配置，例如 Redis 和 MongoDB 数据库的支持、开发常用工具类等，进一步提升开发效率。

---

通过上述步骤，您可以轻松地使用 `FastAPI-APP-Manage` 工具来启动和管理 FastAPI 项目，享受高效便捷的开发体验。




