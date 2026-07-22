from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RepoIntel"
    APP_ENV: str
    APP_VERSION: str = "1.0.0"
    DEBUG: bool

    HOST:str
    PORT:int

    REDIS_HOST:str
    REDIS_PORT:int
    REDIS_DB:int 

    STORAGE_PATH: str

   # STORAGE_ROOT= storage
   #REPOSITORY_PATH= storage/repositories
   #INDEX_PATH= storage/indexes
   #CACHE_PATH= storage/cache

    LOG_LEVEL: str


model_config: SettingsConfigDict =SettingsConfigDict (env_file = ".env")




settings = Settings()
