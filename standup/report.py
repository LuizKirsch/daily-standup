import config
from utils.dates import get_lookback_range, shift_date
from jira.queries import get_current_user, search_issues, get_issue_changelog, get_issue_comments
from jira.parser import extract_status_changes, extract_my_comments


def _jql_status_changed(project: str, after: str, before: str) -> str:
    return (
        f'project = "{project}" AND status CHANGED BY currentUser() '
        f'AFTER "{after}" BEFORE "{before}"'
    )


def _jql_updated(project: str, date_from: str, date_to: str) -> str:
    return (
        f'project = "{project}" '
        f'AND (assignee = currentUser() OR reporter = currentUser()) '
        f'AND updated >= "{date_from}" AND updated <= "{date_to}"'
    )


def _jql_in_progress(project: str) -> str:
    statuses = (
        '"In Progress", "Em Andamento", "Em Progresso", '
        '"In Development", "Em Desenvolvimento", "Doing", "Fazendo"'
    )
    return f'project = "{project}" AND assignee = currentUser() AND status in ({statuses})'


def build(on_progress=None) -> dict:
    user = get_current_user()
    account_id = user["accountId"]
    display_name = user.get("displayName", config.JIRA_EMAIL)

    date_from, date_to, since, until = get_lookback_range()

    after_date = shift_date(date_from, -1)
    before_date = shift_date(date_to, 1)

    status_issues = search_issues(
        _jql_status_changed(config.PROJECT_KEY, after_date, before_date),
        fields=["summary", "status"],
    )
    comment_issues = search_issues(
        _jql_updated(config.PROJECT_KEY, date_from, date_to),
        fields=["summary", "status"],
    )
    in_progress_issues = search_issues(
        _jql_in_progress(config.PROJECT_KEY),
        fields=["summary", "status", "priority", "issuetype"],
    )

    if on_progress:
        on_progress(len(status_issues), len(comment_issues))

    status_changes_by_issue = {}
    for i, issue in enumerate(status_issues, 1):
        key = issue["key"]
        if on_progress:
            on_progress(None, None, changelog=(i, len(status_issues), key))
        histories = get_issue_changelog(key)
        changes = extract_status_changes(histories, account_id, since, until)
        if changes:
            status_changes_by_issue[key] = {
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
                "changes": changes,
            }

    comments_by_issue = {}
    for i, issue in enumerate(comment_issues, 1):
        key = issue["key"]
        if on_progress:
            on_progress(None, None, comments=(i, len(comment_issues), key))
        my_comments = extract_my_comments(get_issue_comments(key), account_id, since, until)
        if my_comments:
            comments_by_issue[key] = {
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
                "comments": my_comments,
            }

    return {
        "user": display_name,
        "date_from": date_from,
        "date_to": date_to,
        "status_changes": status_changes_by_issue,
        "comments": comments_by_issue,
        "in_progress": in_progress_issues,
    }
