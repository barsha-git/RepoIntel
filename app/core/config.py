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

    EMBEDDING_MODEL_NAME: str

    EMBEDDING_MODEL_DEVICE: str

    REDIS_URL: str
    HISTORY_TTL: int
    HISTORY_KEY_PREFIX: str

    LLM_MODEL: str
    LLM_TEMPERATURE: float
    LLM_MAX_TOKENS: int
    LLM_PROVIDERS:str
    GROQ_API_KEY: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")




settings = Settings()
