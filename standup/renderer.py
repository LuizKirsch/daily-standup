from datetime import datetime
import config
from utils.dates import day_label

BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
DIM = "\033[2m"


def _separator(char="─", width=60):
    print(f"{DIM}{char * width}{RESET}")


def _fmt_date(d: str) -> str:
    return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y (%A)")


def _issue_url(key: str) -> str:
    return f"{config.JIRA_URL}/browse/{key}"


def _section(title: str, icon: str):
    print()
    print(f"{BOLD}{icon}  {title}{RESET}")
    _separator()


def render(report: dict):
    date_from = report["date_from"]
    date_to = report["date_to"]
    label = _fmt_date(date_from) if date_from == date_to else f"{_fmt_date(date_from)}  →  {_fmt_date(date_to)}"

    print()
    print(f"{BOLD}{CYAN}{'━' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  DAILY STANDUP  —  {label}{RESET}")
    print(f"{BOLD}{CYAN}  Projeto: {config.PROJECT_KEY}{RESET}")
    print(f"{BOLD}{CYAN}{'━' * 60}{RESET}")
    print(f"  {DIM}Usuário: {report['user']}{RESET}")

    _section("CARDS COM MUDANÇA DE STATUS", "🔄")
    if report["status_changes"]:
        for key, info in report["status_changes"].items():
            print(f"  {BOLD}{YELLOW}{key}{RESET}  {info['summary']}")
            for ch in info["changes"]:
                tag = day_label(ch["at"])
                print(f"    {CYAN}{tag}{RESET} {DIM}{ch['at'][11:]}{RESET}  {ch['from']}  →  {GREEN}{ch['to']}{RESET}")
            print(f"    {DIM}{_issue_url(key)}{RESET}")
            print()
    else:
        print(f"  {DIM}Nenhuma mudança de status registrada.{RESET}")

    _section("CARDS COMENTADOS", "💬")
    if report["comments"]:
        for key, info in report["comments"].items():
            print(f"  {BOLD}{YELLOW}{key}{RESET}  {info['summary']}")
            for c in info["comments"]:
                tag = day_label(c["at"])
                print(f"    {CYAN}{tag}{RESET} {DIM}{c['at'][11:]}{RESET}  \"{c['text']}\"")
            print(f"    {DIM}{_issue_url(key)}{RESET}")
            print()
    else:
        print(f"  {DIM}Nenhum comentário adicionado.{RESET}")

    _section("EM PROGRESSO — ATRIBUÍDOS A MIM", "🚧")
    if report["in_progress"]:
        for issue in report["in_progress"]:
            key = issue["key"]
            fields = issue["fields"]
            priority = fields.get("priority", {}).get("name", "")
            print(f"  {BOLD}{YELLOW}{key}{RESET}  {fields['summary']}")
            print(f"    Status: {GREEN}{fields['status']['name']}{RESET}  {DIM}| Prioridade: {priority}{RESET}")
            print(f"    {DIM}{_issue_url(key)}{RESET}")
            print()
    else:
        print(f"  {DIM}Nenhum card em progresso atribuído a você.{RESET}")

    print()
    _separator("━")
    total_moved = len(report["status_changes"])
    total_commented = len(report["comments"])
    total_wip = len(report["in_progress"])
    print(
        f"  {BOLD}Resumo:{RESET} "
        f"{MAGENTA}{total_moved} movimentados{RESET} · "
        f"{CYAN}{total_commented} comentados{RESET} · "
        f"{GREEN}{total_wip} em progresso{RESET}"
    )
    _separator("━")
    print()
