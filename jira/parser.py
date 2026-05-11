from utils.dates import date_in_range


def extract_text(body) -> str:
    if isinstance(body, str):
        return body
    if isinstance(body, dict):
        node_type = body.get("type")
        if node_type == "text":
            return body.get("text", "")
        if node_type == "mention":
            return body.get("attrs", {}).get("text", "")
        parts = [extract_text(child) for child in body.get("content", [])]
        return " ".join(p for p in parts if p).strip()
    return ""


def extract_status_changes(histories: list, account_id: str, since: str, until: str) -> list:
    changes = []
    for history in histories:
        created = history.get("created", "")
        if history.get("author", {}).get("accountId") != account_id:
            continue
        if not date_in_range(created[:10], since[:10], until[:10]):
            continue
        for item in history.get("items", []):
            if item.get("field") == "status":
                changes.append({
                    "from": item.get("fromString", "?"),
                    "to": item.get("toString", "?"),
                    "at": created[:16].replace("T", " "),
                })
    return changes


def extract_my_comments(comments: list, account_id: str, since: str, until: str) -> list:
    result = []
    for comment in comments:
        if comment.get("author", {}).get("accountId") != account_id:
            continue
        created = comment.get("created", "")
        if not date_in_range(created[:10], since[:10], until[:10]):
            continue
        text = extract_text(comment.get("body", {}))
        short_text = text[:120] + "..." if len(text) > 120 else text
        result.append({"text": short_text, "at": created[:16].replace("T", " ")})
    return result
