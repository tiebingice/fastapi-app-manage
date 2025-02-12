from enum import Enum


class PackageManager(Enum):
    PIP = "pip"
    POETRY = "poetry"
    UV= "uv"


class DataBaseFramework(Enum):
    TORTOISEORM = "tortoise-orm"
    SQLMODEL = "sqlmodel"
    NONE = "none"


class Database(Enum):
    POSTGRES = "PostgreSQL"
    MYSQL = "MySQL"




