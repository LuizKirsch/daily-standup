import os
import sys
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
PROJECT_KEY = "ERPK"

TEAMS_API_URL = os.getenv("TEAMS_API_URL", "")
TEAMS_TO = os.getenv("TEAMS_TO", "")


def validate():
    missing = [v for v in ("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN") if not os.getenv(v)]
    if missing:
        print(f"Erro: variáveis de ambiente ausentes: {', '.join(missing)}")
        print("Copie .env.example para .env e preencha as credenciais.")
        sys.exit(1)
