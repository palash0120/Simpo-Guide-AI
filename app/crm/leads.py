from datetime import date, timedelta

from app.config import settings
from app.crm.client import post

LIST_PATH = "/crm/lead/v2/list"
MAX_LIMIT = 20


def mask_phone(phone: str | None) -> str:
    if not phone:
        return ""
    digits = phone.strip()
    if len(digits) <= 4:
        return "x" * len(digits)
    return digits[:2] + "x" * (len(digits) - 4) + digits[-2:]


def mask_email(email: str | None) -> str:
    if not email or "@" not in email:
        return ""
    name, domain = email.split("@", 1)
    return f"{name[:1]}***@{domain}"


def _message(lead: dict) -> str:
    """Customer's free-text message from the custom fields (data, not instructions)."""
    for field in lead.get("fieldData") or []:
        if field.get("fieldName") == "Message" and field.get("fieldValue"):
            return str(field["fieldValue"])[:150]
    return ""


def _trim(lead: dict) -> dict:
    info = lead.get("personalInfo") or {}
    stage = lead.get("pipelineStage") or {}
    return {
        "reference_no": lead.get("referenceNo"),
        "id": lead.get("id"),
        "name": info.get("name"),
        "phone": mask_phone(info.get("mobile")),
        "email": mask_email(info.get("email")),
        "source": lead.get("leadSource"),
        "stage": stage.get("stageName"),
        "status": stage.get("statusName"),
        "assigned_to": lead.get("staffName"),
        "created_at": lead.get("createdTimeStamp"),
        "message": _message(lead),
    }


def search_leads(
    keyword: str = "",
    stage: str | None = None,
    source: str | None = None,
    days: int | None = None,
    limit: int = 10,
) -> dict:
    # TODO verify against the real API: do stageList/source take names or IDs,
    # and which date format do startDate/endDate expect?
    start_date = ""
    end_date = ""
    if days:
        today = date.today()
        start_date = (today - timedelta(days=days)).isoformat()
        end_date = today.isoformat()

    payload = {
        "pageNo": 0,
        "size": max(1, min(limit, MAX_LIMIT)),
        "businessId": settings.business_id,  # fixed from .env, never from the LLM
        "type": "LEAD",
        "searchText": keyword.strip(),
        "stageId": "",
        "pipelineId": "",
        "statusList": [],
        "source": [source] if source else [],
        "stageList": [stage] if stage else [],
        "staffId": [],
        "startDate": start_date,
        "endDate": end_date,
        "campaignIds": [],
        "isPagination": True,
        "sortByCreatedTimeStamp": True,
        "sortBy": "",
        "sortAsc": None,
    }

    data = post(LIST_PATH, payload)
    leads = [_trim(item) for item in data.get("content", [])]
    return {
        "total": data.get("totalElements", len(leads)),
        "showing": len(leads),
        "leads": leads,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(search_leads(limit=5), indent=2, default=str))
