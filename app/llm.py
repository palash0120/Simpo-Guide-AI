from langchain_core.language_models.chat_models import BaseChatModel

from app.config import settings


def get_llm() -> BaseChatModel:
    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
        )
    raise ValueError(f"Unknown LLM_PROVIDER: {settings.llm_provider}")
