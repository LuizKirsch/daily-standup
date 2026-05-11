import requests
from jira import client


def get_current_user() -> dict:
    return client.get("/myself")


def search_issues(jql: str, fields: list, max_results: int = 100) -> list:
    results = []
    next_page_token = None
    while True:
        body = {"jql": jql, "fields": fields, "maxResults": max_results}
        if next_page_token:
            body["nextPageToken"] = next_page_token
        data = client.post("/search/jql", body)
        results.extend(data.get("issues", []))
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    return results


def get_issue_changelog(issue_key: str) -> list:
    try:
        data = client.get(f"/issue/{issue_key}/changelog")
        return data.get("values", [])
    except requests.HTTPError:
        return []


def get_issue_comments(issue_key: str) -> list:
    try:
        data = client.get(f"/issue/{issue_key}/comment", params={"maxResults": 100})
        return data.get("comments", [])
    except requests.HTTPError:
        return []
