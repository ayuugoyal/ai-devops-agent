# MCP Remote Server Manager

<div align="center">

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg?style=for-the-badge)

**AI-powered remote server management through Claude Desktop or any MCP Client**

</div>


## 📖 Overview

MCP Remote Server Manager is a Model Context Protocol (MCP) server that enables AI assistants like Claude to manage remote servers (VPS, Raspberry Pi, etc.) through SSH. Perfect for DevOps automation, AI-driven infrastructure management, and LLMOps workflows.

### 🎯 Use Cases

- **DevOps Automation**: Let AI handle routine server maintenance
- **LLMOps**: Manage ML model deployments on remote servers
- **AIOps**: Intelligent monitoring and incident response
- **Multi-Server Management**: Control multiple servers from Claude Desktop

### ✨ Features

- 🔐 **Secure SSH Connections** - Password and SSH key authentication
- 📦 **PM2 Management** - Start, stop, restart, and monitor Node.js applications
- 📁 **File Operations** - Read, list, and manage files remotely
- 📊 **System Monitoring** - CPU, memory, disk usage, and uptime tracking
- 🖥️ **Custom Commands** - Execute any shell command on remote servers
- 🐳 **Docker Ready** - Pull and run from Docker Hub in seconds
- 🔄 **Multi-Server Support** - Manage unlimited servers simultaneously


## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

**Pull the pre-built image from Docker Hub:**

```bash
docker pull ayuugoyal/mcp-remote-server:latest
```

**Create a `.env` file with your server credentials:**

```bash
SERVER_1_ID=production
SERVER_1_HOST=your-server.com
SERVER_1_USER=root
SERVER_1_PASSWORD=your-password
```

**Add to your Claude Desktop config:**

**Path:**
- macOS/Linux: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "remote-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/absolute/path/to/your/.env",
        "ayuugoyal/mcp-remote-server:latest"
      ]
    }
  }
}
```

**Or test it directly:**

```bash
docker run -it --rm \
  -e SERVER_1_HOST=your-server.com \
  -e SERVER_1_USER=root \
  -e SERVER_1_PASSWORD=your-password \
  ayuugoyal/mcp-remote-server:latest
```

**With SSH keys:**

```bash
docker run -it --rm \
  -e SERVER_1_HOST=your-server.com \
  -e SERVER_1_USER=root \
  -e SERVER_1_KEY_FILE=/root/.ssh/id_rsa \
  -v ~/.ssh:/root/.ssh:ro \
  ayuugoyal/mcp-remote-server:latest
```


### Option 2: Manual Installation

```bash
git clone https://github.com/ayuugoyal/mcp-remote-server.git
cd mcp-remote-server
pip install -r requirements.txt
cp .env.example .env
python -m src.server
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `SERVER_1_ID` | Unique identifier for server | No | `server_1` | `production` |
| `SERVER_1_HOST` | Server IP or domain | **Yes** | - | `192.168.1.100` |
| `SERVER_1_USER` | SSH username | No | `root` | `admin` |
| `SERVER_1_PASSWORD` | SSH password | Yes* | - | `SecurePass123` |
| `SERVER_1_KEY_FILE` | Path to SSH private key | Yes* | - | `/root/.ssh/id_rsa` |
| `SERVER_1_PORT` | SSH port | No | `22` | `2222` |

*Either `PASSWORD` or `KEY_FILE` is required

**For multiple servers:** Use `SERVER_2_*`, `SERVER_3_*`, etc.


<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for the AI and DevOps community

</div>