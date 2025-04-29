from pydantic_settings import BaseSettings
from functools import lru_cache

class GA4Config(BaseSettings):
    measurement_id: str
    api_secret: str
    stream_id: str
    
    class Config:
        env_file = ".env"
        env_prefix = "GA4_"

@lru_cache()
def get_ga4_config() -> GA4Config:
    return GA4Config() 