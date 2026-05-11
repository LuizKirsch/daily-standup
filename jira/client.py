import sys
import requests
from requests.auth import HTTPBasicAuth
import config


def _auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(config.JIRA_EMAIL, config.JIRA_API_TOKEN)


def _handle_401(resp: requests.Response):
    if resp.status_code == 401:
        print("Erro 401: credenciais inválidas. Verifique JIRA_EMAIL e JIRA_API_TOKEN no .env")
        sys.exit(1)


def get(path: str, params: dict = None) -> dict:
    url = f"{config.JIRA_URL}/rest/api/3{path}"
    resp = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=_auth(),
        params=params,
        timeout=15,
    )
    _handle_401(resp)
    resp.raise_for_status()
    return resp.json()


def post(path: str, body: dict) -> dict:
    url = f"{config.JIRA_URL}/rest/api/3{path}"
    resp = requests.post(
        url,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
        json=body,
        timeout=15,
    )
    _handle_401(resp)
    if not resp.ok:
        print(f"Erro {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()
