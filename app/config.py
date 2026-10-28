from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str
    llm_provider: str = "gemini"
    llm_model: str
    mongo_uri: str
    mongo_db_name: str = "crm"
    business_id: str
    simpo_api_base_url: str = "https://stage-api.simpo.ai"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
