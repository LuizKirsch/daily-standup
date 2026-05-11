import sys
sys.stdout.reconfigure(encoding="utf-8")

import config
from standup import report as standup_report
from standup import renderer
from utils import teams

DIM = "\033[2m"
RESET = "\033[0m"


def _on_progress(status_count, comment_count, changelog=None, comments=None):
    if status_count is not None:
        print(f"{DIM}  {status_count} movimentações · {comment_count} para checar comentários{RESET}")
    elif changelog:
        i, total, key = changelog
        print(f"{DIM}  changelog [{i}/{total}] {key}...{RESET}", end="\r")
    elif comments:
        i, total, key = comments
        print(f"{DIM}  comentários [{i}/{total}] {key}...{RESET}", end="\r")


def main():
    config.validate()
    print(f"{DIM}Conectando ao Jira em {config.JIRA_URL}...{RESET}")
    report = standup_report.build(on_progress=_on_progress)
    renderer.render(report)
    teams.send(report)


if __name__ == "__main__":
    main()
