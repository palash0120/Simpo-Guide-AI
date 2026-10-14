from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str
    llm_provider: str = "gemini"
    llm_model: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
