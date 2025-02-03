
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
    def tortoise_config(self):
        return {
            'connections': {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.mysql', #note: Replace according to the used database version, here we do not directly write the corresponding driver.
                    'credentials': {
                        'host': self.db_host,
                        'port': self.db_port,
                        'user': self.db_user,
                        'password': self.db_password,
                        'database': self.database,
                    }
                },
        
            },
            'apps': {
                'models': {
                    'models': ['app.models'],
                    'default_connection': 'default',
                }
            }
        }

        


settings = Settings()
