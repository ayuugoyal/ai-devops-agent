# AI DevOps Agent

<div align="center">

![MCP](https://img.shields.io/badge/MCP-Official%20SDK-green.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-Bot-4A154B.svg?style=for-the-badge&logo=slack&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-67%2B%20MCP%20Servers-FF9900.svg?style=for-the-badge&logo=amazonaws&logoColor=white)

**Your AI-native DevOps engineer. Connect to any cloud, any server, from Slack, terminal, or Claude.**

[Setup](#-quick-setup) · [Integrations](#-supported-integrations) · [Slack](#-slack-integration) · [Claude Desktop](#-claude-desktop) · [Architecture](#-architecture)

</div>

---

## What Is This?

AI DevOps Agent is a **self-hosted MCP server** that acts as a full DevOps engineer you can talk to. It bridges your infrastructure — cloud providers, SSH servers, Docker, Kubernetes — into a single AI agent accessible from Slack, Claude Desktop, Claude Web, or a terminal.

**You talk to it naturally:**
```
"Deploy the main branch to prod and restart the API service"
"Check AWS costs this month and show me what's spiking"
"Tail the nginx error logs on server-1 and find any 500s from the last hour"
"Rollback the last 2 commits on staging and alert me in Slack"
```

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                      TRIGGER INTERFACES                               │
│                                                                       │
│  ┌─────────────┐  ┌────────────────┐  ┌────────────┐  ┌──────────┐  │
│  │  Slack Bot  │  │ Claude Desktop │  │ Claude Web │  │ Terminal │  │
│  │ /devops ... │  │  (stdio MCP)   │  │ (SSE/HTTP) │  │   CLI    │  │
│  └──────┬──────┘  └───────┬────────┘  └─────┬──────┘  └────┬─────┘  │
│         └─────────────────┴────────┬─────────┘              │        │
│                                    │◄───────────────────────┘        │
│                          ┌─────────▼──────────┐                      │
│                          │  AI DevOps Agent    │                      │
│                          │  FastMCP Server     │                      │
│                          │  (src/server.py)    │                      │
│                          └────────┬────────────┘                      │
│                 ┌─────────────────┼──────────────────┐               │
│                 │                 │                  │               │
│    ┌────────────▼──────┐  ┌───────▼────────┐  ┌──────▼──────────┐   │
│    │  Built-in Tools   │  │  MCP Proxy     │  │  Config Store   │   │
│    │                   │  │  Layer         │  │  ~/.devops-agent│   │
│    │ • SSH Management  │  │                │  │  /config.json   │   │
│    │ • Docker/Compose  │  │ Official MCP   │  │  + OS Keyring   │   │
│    │ • Git & Deploy    │  │ servers you    │  │  (secrets)      │   │
│    │ • Log Monitoring  │  │ selected:      │  └─────────────────┘   │
│    │ • Health Checks   │  │                │                         │
│    │ • Systemd/PM2     │  │ • AWS (67+)    │                         │
│    │ • Networking      │  │ • Grafana      │                         │
│    │ • Cron Jobs       │  │ • GitHub       │                         │
│    │ • Env Files       │  │ • Kubernetes   │                         │
│    └───────────────────┘  │ • PagerDuty    │                         │
│                           │ • Datadog      │                         │
│                           └────────────────┘                         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Supported Integrations

### AWS — 67+ Official MCP Servers (by awslabs)

Run `devops-agent setup` and select any of these:

| Category | MCP Server | What it does |
|---|---|---|
| **Cost** | `billing-cost-management` | Bills, invoices, usage reports |
| **Cost** | `cost-explorer` | Cost & usage queries, forecasts |
| **Cost** | `aws-pricing` | Service pricing lookup |
| **Compute** | `ecs-mcp-server` | ECS clusters, services, tasks |
| **Compute** | `eks-mcp-server` | EKS clusters, node groups, pods |
| **Compute** | `lambda-tool` | Invoke, deploy, manage Lambda functions |
| **Compute** | `sagemaker-ai` | SageMaker training, endpoints, models |
| **Storage** | `s3-tables` | S3 bucket and table operations |
| **Database** | `dynamodb` | DynamoDB tables, queries, scans |
| **Database** | `redshift` | Redshift clusters, query execution |
| **Database** | `aurora-dsql` | Aurora DSQL operations |
| **Database** | `documentdb` | DocumentDB management |
| **Database** | `elasticache` | ElastiCache clusters, replication |
| **Observability** | `cloudwatch` | Metrics, alarms, dashboards |
| **Observability** | `cloudwatch-applicationsignals` | APM signals & SLOs |
| **Observability** | `cloudtrail` | API audit logs, events |
| **Observability** | `prometheus` | Prometheus metrics (AWS Managed) |
| **Networking** | `aws-network` | VPCs, subnets, security groups |
| **Messaging** | `amazon-sns-sqs` | Topics, queues, publish/subscribe |
| **IAC** | `cdk-mcp-server` | CDK app generation & deployment |
| **IAC** | `cfn-mcp-server` | CloudFormation stacks |
| **IAC** | `terraform-mcp-server` | Terraform plans and applies |
| **IAC** | `aws-iac` | Generic IaC operations |
| **AI/ML** | `bedrock-kb-retrieval` | Bedrock Knowledge Base queries |
| **Serverless** | `aws-serverless` | SAM, serverless deployments |
| **Serverless** | `stepfunctions-tool` | Step Functions state machines |
| **Security** | `iam-mcp-server` | IAM roles, policies, users |
| **Security** | `well-architected-security` | Security best practices checks |
| **Support** | `aws-support` | AWS Support tickets |
| **Docs** | `aws-documentation` | AWS docs search & retrieval |
| _...and 37 more_ | | |

### Other Providers

| Provider | What it does |
|---|---|
| **Grafana** | Dashboards, alerts, datasource queries, annotations |
| **GitHub** | PRs, issues, Actions workflows, code search |
| **Kubernetes** | Pods, deployments, logs, manifests, scaling |
| **PagerDuty** | Incidents, escalations, on-call schedules |
| **Datadog** | Metrics, monitors, logs, APM traces |

---

## Quick Setup

```bash
git clone https://github.com/ayuugoyal/ai-devops-agent
cd ai-devops-agent
pip install -e .
devops-agent-setup
```

The setup wizard walks you through everything interactively:

```
AI DevOps Agent — Setup
━━━━━━━━━━━━━━━━━━━━━━━

Step 1/6  Select cloud providers
  [x] AWS
  [ ] GCP
  [x] GitHub
  [x] Grafana
  [ ] Kubernetes
  [ ] PagerDuty
  [ ] Datadog

Step 2/6  Select AWS MCP servers to enable
  [x] Cost Explorer & Billing
  [x] CloudWatch (metrics + logs)
  [x] ECS
  [ ] EKS
  [x] Lambda
  [ ] SageMaker
  ...

Step 3/6  AWS Credentials
  AWS Access Key ID: ****
  AWS Secret Access Key: ****
  Default Region [us-east-1]: ap-south-1

Step 4/6  SSH Servers
  Add a server? (y/n): y
  Host: 10.0.0.5
  Username: deploy
  Auth (key/password): key
  Key path [~/.ssh/id_rsa]:

Step 5/6  Slack Integration
  Enable Slack bot? (y/n): y
  Slack Bot Token (xoxb-...): ****
  Slack App Token (xapp-...): ****
  Allowed channel IDs: C0123DEVOPS

Step 6/6  How will you connect?
  (o) Claude Desktop  → writes claude_desktop_config.json automatically
  ( ) Claude Web      → starts HTTP server, optionally sets up Cloudflare Tunnel
  ( ) Both

✓ Config saved to ~/.devops-agent/config.json
✓ Secrets stored in macOS Keychain
✓ Claude Desktop config updated
```

---

## Slack Integration

The Slack bot lets your whole team trigger the agent from any channel.

### Setup Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → Create New App → From Manifest
2. Paste this manifest:

```yaml
display_information:
  name: DevOps Agent
features:
  slash_commands:
    - command: /devops
      description: Talk to your AI DevOps Agent
      usage_hint: "[deploy|rollback|health|logs|aws|docker] ..."
  bot_user:
    display_name: devops-agent
settings:
  socket_mode_enabled: true
  event_subscriptions:
    bot_events:
      - message.channels
```

3. Install to workspace, copy **Bot Token** (`xoxb-...`) and **App Token** (`xapp-...`)
4. Run `devops-agent-setup` and enter the tokens when prompted

### Usage from Slack

```
/devops health prod-1
/devops deploy prod-1 /var/www/app main
/devops rollback prod-1 /var/www/app 2
/devops logs prod-1 tail /var/log/nginx/error.log
/devops docker containers prod-1
/devops aws costs this month
/devops aws cloudwatch errors last 1h
```

The bot responds in the channel with formatted output.

---

## Claude Desktop

After setup, Claude Desktop config is auto-written. Or add manually:

**`~/Library/Application Support/Claude/claude_desktop_config.json`**

```json
{
  "mcpServers": {
    "ai-devops-agent": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--env-file", "/absolute/path/to/.env",
        "-v", "~/.devops-agent:/root/.devops-agent:ro",
        "-v", "~/.ssh:/root/.ssh:ro",
        "ayuugoyal/ai-devops-agent:latest"
      ]
    }
  }
}
```

Or without Docker (after `pip install -e .`):

```json
{
  "mcpServers": {
    "ai-devops-agent": {
      "command": "devops-agent",
      "env": {
        "SERVER_1_HOST": "your-server.com",
        "SERVER_1_USER": "root",
        "SERVER_1_PASSWORD": "your-password"
      }
    }
  }
}
```

---

## Claude Web (Remote MCP)

Run the agent in HTTP/SSE mode:

```bash
AGENT_MODE=sse PORT=8080 devops-agent
```

For a public URL (no port forwarding needed), use Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:8080
# → https://xxxx.trycloudflare.com
```

Then in Claude Web → Settings → MCP Servers → Add:
```
https://xxxx.trycloudflare.com
```

---

## Docker

```bash
# Stdio mode (for Claude Desktop)
docker run -i --rm \
  --env-file .env \
  -v ~/.devops-agent:/root/.devops-agent:ro \
  ayuugoyal/ai-devops-agent:latest

# HTTP/SSE mode (for Claude Web / remote)
docker run -p 8080:8080 \
  -e AGENT_MODE=sse \
  --env-file .env \
  -v ~/.devops-agent:/root/.devops-agent:ro \
  ayuugoyal/ai-devops-agent:latest

# With Slack bot
docker compose --profile slack up
```

---

## Built-in Tools Reference

| Category | Tools |
|---|---|
| **Servers** | `list_servers`, `connect_server`, `disconnect_server` |
| **System** | `system_info`, `run_command`, `health_check` |
| **Files** | `list_files`, `read_file`, `write_file` |
| **Docker** | `docker_manage` (containers/images/stats/prune), `compose_manage` (up/down/logs) |
| **Deploy** | `deploy` (auto-detect Node/Python), `rollback`, `git_manage`, `env_manage` |
| **Services** | `service_manage` (systemd), `pm2_manage`, `process_manage` |
| **Logs** | `log_manage` (tail/search/errors/journal/nginx) |
| **Network** | `network_manage` (ping/curl/ssl/dns/firewall), `port_check`, `cron_manage` |

---

## Environment Variables

```bash
# SSH Servers (add SERVER_2_*, SERVER_3_* for more)
SERVER_1_ID=prod
SERVER_1_HOST=your-server.com
SERVER_1_USER=root
SERVER_1_PASSWORD=your-password    # or use SERVER_1_KEY_FILE
SERVER_1_PORT=22

# Agent mode
AGENT_MODE=stdio                   # stdio (default) or sse

# Slack (if using bot)
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

All cloud credentials (AWS keys, Grafana tokens, etc.) are stored in the OS keyring by `devops-agent-setup`, not in the `.env` file.

---

## Project Structure

```
ai-devops-agent/
├── src/
│   ├── server.py              # FastMCP server — all tools registered here
│   ├── ssh_manager.py         # Paramiko SSH abstraction
│   ├── config/
│   │   ├── settings.py        # Env + config.json loader
│   │   └── store.py           # ~/.devops-agent/config.json read/write
│   ├── registry/
│   │   └── mcp_registry.py    # All known MCP servers (AWS, Grafana, GitHub...)
│   ├── credentials/
│   │   └── vault.py           # OS keyring + encrypted file fallback
│   ├── mcp_clients/
│   │   ├── proxy_manager.py   # Launches external MCP subprocesses
│   │   └── tool_bridge.py     # Forwards external tools into FastMCP
│   ├── slack/
│   │   ├── bot.py             # slack-bolt Socket Mode app
│   │   └── handler.py         # Command → tool dispatch
│   ├── tools/
│   │   ├── docker_tools.py
│   │   ├── deploy_tools.py
│   │   ├── log_tools.py
│   │   ├── network_tools.py
│   │   ├── service_tools.py
│   │   └── ...
│   └── interfaces/
│       └── http_server.py     # SSE transport for Claude Web
└── setup_cli/
    ├── wizard.py              # questionary-based interactive setup
    ├── provider_selector.py   # Cloud + MCP picker menus
    └── configurator.py        # Writes config, generates Claude Desktop JSON
```

---

## Roadmap

- [x] SSH server management
- [x] Docker & Compose management
- [x] Git deployments & rollback
- [x] Log monitoring & analysis
- [x] Health checks & network diagnostics
- [x] Systemd / PM2 / process management
- [ ] `devops-agent setup` interactive CLI wizard
- [ ] AWS MCP proxy layer (67 official servers)
- [ ] Grafana / GitHub / K8s MCP proxy
- [ ] Slack bot integration
- [ ] Claude Web SSE/HTTP mode
- [ ] Cloudflare Tunnel auto-setup
- [ ] Web UI dashboard

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Built with the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) · Made for the AI × DevOps community

</div>
