import tomlkit


def write_dict_to_toml(toml_dict: dict, flag: bool = False, fastapi_version_str: str = None):
    """
    更新 pyproject.toml 文件中的 dependencies 部分，同时保留文件的其他部分不变。

    :param toml_dict: 包含所有依赖项的字典
    :param flag: 是否启用 fastapi[standard] 的内联表格格式
    :param fastapi_version_str: 如果 flag=True，则指定 fastapi 的版本号
    """
    # 读取现有的 pyproject.toml 文件内容
    with open('pyproject.toml', 'r') as f:
        doc = tomlkit.parse(f.read())

    # 检查并确保 [tool.poetry.dependencies] 表存在
    if 'tool' not in doc or 'poetry' not in doc['tool'] or 'dependencies' not in doc['tool']['poetry']:
        raise ValueError("pyproject.toml 文件中缺少必要的 [tool.poetry.dependencies] 表")

    dependencies = doc['tool']['poetry']['dependencies']

    if flag:
        dependencies["fastapi"] = tomlkit.inline_table()
        dependencies["fastapi"].update({
            'extras': ['standard'],
            'version': "^" + fastapi_version_str
        })

    dependencies.update(toml_dict)

    with open('pyproject.toml', 'w') as f:
        f.write(tomlkit.dumps(doc))
