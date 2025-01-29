import tomlkit
from typing import cast

def write_dict_to_toml(toml_dict: dict, flag: bool = False, fastapi_version_str: str|None = None):
    """
    Update the dependencies section of the pyproject.toml file while keeping the rest of the file unchanged.

    :param toml_dict: Dictionary containing all dependencies
    :param flag: Whether to enable the inline table format for fastapi[standard]
    :param fastapi_version_str: If flag=True, specify the version number for fastapi
    """
    # Read the existing content of the pyproject.toml file
    with open('pyproject.toml', 'r', encoding="utf-8") as f:
        doc = cast(dict,tomlkit.parse(f.read()))

    # Check and ensure that the [tool.poetry.dependencies] table exists
    if 'tool' not in doc or 'poetry' not in doc['tool'] or 'dependencies' not in doc['tool']['poetry']: 
        raise ValueError("The pyproject.toml file is missing the required [tool.poetry.dependencies] table")

    dependencies = doc['tool']['poetry']['dependencies']

    if flag:
        dependencies["fastapi"] = tomlkit.inline_table()
        dependencies["fastapi"].update({
            'extras': ['standard'],
            'version': "^" + cast(str, fastapi_version_str)
        })

    dependencies.update(toml_dict) 

    with open('pyproject.toml', 'w') as f:
        f.write(tomlkit.dumps(doc))
