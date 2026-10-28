from typing import Optional

from langchain_core.tools import tool

from app.crm.client import CrmApiError
from app.crm.leads import search_leads as _search_leads


@tool
def search_leads(
    keyword: str = "",
    stage: Optional[str] = None,
    source: Optional[str] = None,
    days: Optional[int] = None,
    limit: int = 10,
) -> dict:
    """Search CRM leads. Use for questions about leads, such as listing recent
    leads, finding a lead by name, phone number or reference number (like L080),
    or filtering by stage or source.

    Args:
        keyword: Name, phone number or reference number to search for. Empty for no text filter.
        stage: Pipeline stage name, for example "New". Leave empty unless the user asks for a stage.
        source: Where the lead came from, for example "Instagram" or "WEBSITE".
        days: Only leads created in the last N days. "This week" means 7.
        limit: How many leads to return, 1 to 20. Default 10.

    Returns total (all matches), showing (how many returned) and the leads.
    Phone and email are masked. This tool only reads data and never changes it.
    """
    try:
        return _search_leads(
            keyword=keyword, stage=stage, source=source, days=days, limit=limit
        )
    except CrmApiError as e:
        return {"error": str(e)}
