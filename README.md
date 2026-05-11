# Daily Standup — Jira ERPK

Gera um resumo de standup diário no terminal com as atividades do dia anterior no projeto ERPK.

## O que é exibido

- **Cards com mudança de status** — issues que você moveu entre colunas ontem
- **Cards comentados** — issues em que você adicionou comentários ontem
- **Em progresso atribuídos a mim** — todos os cards atualmente em andamento na sua fila

## Setup

### 1. Pré-requisitos

- Python 3.9+

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciais

```bash
copy .env.example .env
```

Edite o `.env` com suas credenciais:

```env
JIRA_URL=sua-url-jira-aqui
JIRA_EMAIL=seu-email@wject.com
JIRA_API_TOKEN=seu-api-token
```

**Como gerar o API Token:**
1. Acesse https://id.atlassian.com/manage-profile/security/api-tokens
2. Clique em **Create API token**
3. Dê um nome (ex: `daily-standup`) e copie o token gerado
4. Cole no `.env` como `JIRA_API_TOKEN`

### 4. Executar

```bash
python daily-standup.py
```

## Exemplo de saída

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DAILY STANDUP  —  09/05/2026 (sexta-feira)
  Projeto: ERPK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Usuário: Luiz Kirsch

🔄  CARDS COM MUDANÇA DE STATUS
────────────────────────────────────────────────────────────
  ERPK-42  Implementar validação de CPF no cadastro
    2026-05-09 14:23  Em Análise  →  Em Progresso
    https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

💬  CARDS COMENTADOS
────────────────────────────────────────────────────────────
  ERPK-38  Corrigir cálculo de impostos na NF
    2026-05-09 11:05  "Validei com a equipe fiscal, pode seguir..."
    https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

🚧  EM PROGRESSO — ATRIBUÍDOS A MIM
────────────────────────────────────────────────────────────
  ERPK-42  Implementar validação de CPF no cadastro
    Status: Em Progresso  | Prioridade: High
    https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Resumo: 1 movimentados · 1 comentados · 1 em progresso
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```