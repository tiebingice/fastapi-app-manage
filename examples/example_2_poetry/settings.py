
from fastapi_utils.api_settings import APISettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(APISettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    db_host:str="127.0.0.1"
    db_port:int=6379
    db_user:str="root"
    db_password:str="pwd"
    database:str="db"
            
            
    @property
    def database_url(self):
        return f"pymysql+mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}" # #note: Replace according to the used database version, here we do not directly write the corresponding driver.
        


settings = Settings()
