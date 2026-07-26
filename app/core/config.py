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

    Redis_URL: str
    HISTORY_TTL: int
    HISTORY_KEY_PREFIX: str

    LLM_MODEL_NAME: str
    LLM_MODEL_TEMPERATURE: float
    LLM_MODEL_MAX_TOKENS: int
    LLM_PROVIDERS: list[str]
    GROQ_API_KEY: str



model_config: SettingsConfigDict =SettingsConfigDict (env_file = ".env")




settings = Settings()
