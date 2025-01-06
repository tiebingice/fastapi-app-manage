from enum import Enum


class PackageManager(Enum):
    PIP = "pip"
    POETRY = "poetry"


class DataBaseFramework(Enum):
    TORTOISEORM = "tortoise-orm"
    SQLMODEL = "sqlmodel"
    NONE = "none"


class Database(Enum):
    POSTGRES = "PostgresSQL"
    MYSQL = "MySQL"
