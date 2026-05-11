import requests
import config
from utils.dates import day_label


def _issue_url(key: str) -> str:
    return f"{config.JIRA_URL}/browse/{key}"


def format_report(report: dict) -> str:
    from datetime import datetime

    def fmt_date(d: str) -> str:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y (%A)")

    date_from = report["date_from"]
    date_to = report["date_to"]
    period = fmt_date(date_from) if date_from == date_to else f"{fmt_date(date_from)} → {fmt_date(date_to)}"

    def issue_block(key: str, summary: str, rows: list[str]) -> str:
        url = _issue_url(key)
        rows_html = "".join(f"<div style='margin-left:16px;color:#aaa;font-size:13px'>{r}</div>" for r in rows)
        return (
            f"<div style='margin-bottom:10px'>"
            f"<a href='{url}' style='font-weight:bold;color:#64B5F6;text-decoration:none'>{key}</a>"
            f" <span style='color:#e0e0e0'>{summary}</span>"
            f"{rows_html}"
            f"</div>"
        )

    status_html = ""
    if report["status_changes"]:
        for key, info in report["status_changes"].items():
            rows = [
                f"<span style='color:#777'>{day_label(ch['at'])} {ch['at'][11:]}</span>"
                f"&nbsp; <span style='color:#ccc'>{ch['from']}</span> &rarr; <b style='color:#81C784'>{ch['to']}</b>"
                for ch in info["changes"]
            ]
            status_html += issue_block(key, info["summary"], rows)
    else:
        status_html = "<p style='color:#777'>Nenhuma mudança de status.</p>"

    comments_html = ""
    if report["comments"]:
        for key, info in report["comments"].items():
            rows = [
                f"<span style='color:#777'>{day_label(c['at'])} {c['at'][11:]}</span>"
                f"&nbsp; <span style='color:#ccc'>&ldquo;{c['text']}&rdquo;</span>"
                for c in info["comments"]
            ]
            comments_html += issue_block(key, info["summary"], rows)
    else:
        comments_html = "<p style='color:#777'>Nenhum comentário adicionado.</p>"

    wip_html = ""
    if report["in_progress"]:
        for issue in report["in_progress"]:
            key = issue["key"]
            fields = issue["fields"]
            priority = fields.get("priority", {}).get("name", "")
            rows = [f"<span style='color:#aaa'>{fields['status']['name']} · {priority}</span>"]
            wip_html += issue_block(key, fields["summary"], rows)
    else:
        wip_html = "<p style='color:#777'>Nenhum card em progresso.</p>"

    total_moved = len(report["status_changes"])
    total_commented = len(report["comments"])
    total_wip = len(report["in_progress"])

    return f"""<div style='font-family:sans-serif;max-width:680px;color:#e0e0e0'>
  <div style='background:#1565C0;color:#fff;padding:12px 16px;border-radius:6px 6px 0 0'>
    <div style='font-size:16px;font-weight:bold'>📋 Daily Standup — {period}</div>
    <div style='font-size:13px;opacity:.8'>Projeto: {config.PROJECT_KEY} &nbsp;|&nbsp; {report['user']}</div>
  </div>
  <div style='border:1px solid #444;border-top:none;border-radius:0 0 6px 6px;padding:16px'>

    <h3 style='margin:0 0 8px;font-size:14px;color:#90CAF9'>🔄 Cards com mudança de status</h3>
    {status_html}

    <hr style='border:none;border-top:1px solid #444;margin:12px 0'>

    <h3 style='margin:0 0 8px;font-size:14px;color:#90CAF9'>💬 Cards comentados</h3>
    {comments_html}

    <hr style='border:none;border-top:1px solid #444;margin:12px 0'>

    <h3 style='margin:0 0 8px;font-size:14px;color:#90CAF9'>🚧 Em progresso — atribuídos a mim</h3>
    {wip_html}

    <div style='margin-top:12px;padding:8px 12px;border:1px solid #444;border-radius:4px;font-size:13px;color:#aaa'>
      <b style='color:#e0e0e0'>Resumo:</b> {total_moved} movimentados &nbsp;·&nbsp; {total_commented} comentados &nbsp;·&nbsp; {total_wip} em progresso
    </div>
  </div>
</div>"""


def send(report: dict):
    if not config.TEAMS_API_URL or not config.TEAMS_TO:
        return

    message = format_report(report)
    try:
        resp = requests.post(
            config.TEAMS_API_URL,
            json={"to": config.TEAMS_TO, "message": message},
            timeout=10,
        )
        resp.raise_for_status()
        print(f"\033[2mMensagem enviada para {config.TEAMS_TO} no Teams.\033[0m")
    except requests.RequestException as e:
        print(f"\033[93mAviso: não foi possível enviar para o Teams: {e}\033[0m")
