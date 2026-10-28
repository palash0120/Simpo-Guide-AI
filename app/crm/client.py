from functools import lru_cache

import httpx

from app.config import settings


class CrmApiError(Exception):
    """Short, safe error message that can be shown to the LLM and the user."""


@lru_cache(maxsize=1)
def get_http() -> httpx.Client:
    return httpx.Client(base_url=settings.simpo_api_base_url, timeout=15)


def post(path: str, payload: dict) -> dict:
    try:
        response = get_http().put(path, json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # dev only: show the server's real reason in the terminal, never to the LLM
        print(f"CRM API {e.response.status_code}: {e.response.text[:500]}")
        raise CrmApiError(f"CRM service returned an error ({e.response.status_code}).") from None
    except httpx.HTTPError:
        raise CrmApiError("CRM service is not reachable right now.") from None
    except ValueError:
        raise CrmApiError("CRM service returned an unexpected response.") from None
