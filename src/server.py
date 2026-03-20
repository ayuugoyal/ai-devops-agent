"""
AI DevOps Agent — MCP Server
Powered by the official MCP Python SDK (mcp[cli])

Integrates with official MCP servers:
  - AWS MCP (cost analysis, infrastructure)
  - Grafana MCP (dashboards, alerts, metrics)
  - GitHub MCP (PRs, issues, Actions)
  - Kubernetes MCP (cluster management)

Plus built-in SSH-based tools for direct server control.
"""

from mcp.server.fastmcp import FastMCP
from .config.settings import load_servers_from_env
from .tools import (
    list_servers, connect_server, disconnect_server,
    system_info, run_command,
    list_files, read_file, write_file,
    pm2_manage,
    docker_manage, compose_manage,
    git_manage, deploy, rollback, env_manage,
    service_manage, port_check, process_manage,
    log_manage,
    health_check, network_manage, cron_manage,
)

load_servers_from_env()
mcp = FastMCP("ai-devops-agent")


# ── Server Management ─────────────────────────────────────────────────────────

@mcp.tool()
async def list_servers_tool() -> str:
    """List all configured servers and their connection status."""
    result = await list_servers({})
    return result[0]["text"]


@mcp.tool()
async def connect_server_tool(server_id: str) -> str:
    """Connect to a configured remote server via SSH."""
    result = await connect_server({"server_id": server_id})
    return result[0]["text"]


@mcp.tool()
async def disconnect_server_tool(server_id: str) -> str:
    """Disconnect from a remote server."""
    result = await disconnect_server({"server_id": server_id})
    return result[0]["text"]


# ── System ────────────────────────────────────────────────────────────────────

@mcp.tool()
async def system_info_tool(server_id: str) -> str:
    """Get CPU, memory, disk, and uptime info from a remote server."""
    result = await system_info({"server_id": server_id})
    return result[0]["text"]


@mcp.tool()
async def run_command_tool(server_id: str, command: str) -> str:
    """Run any shell command on a remote server."""
    result = await run_command({"server_id": server_id, "command": command})
    return result[0]["text"]


@mcp.tool()
async def health_check_tool(server_id: str) -> str:
    """Full health check: uptime, memory, disk, ports, Docker, failed services."""
    result = await health_check({"server_id": server_id})
    return result[0]["text"]


# ── Files ─────────────────────────────────────────────────────────────────────

@mcp.tool()
async def list_files_tool(server_id: str, path: str = ".") -> str:
    """List files and directories at a path on the remote server."""
    result = await list_files({"server_id": server_id, "path": path})
    return result[0]["text"]


@mcp.tool()
async def read_file_tool(server_id: str, file_path: str) -> str:
    """Read the contents of a file on the remote server."""
    result = await read_file({"server_id": server_id, "file_path": file_path})
    return result[0]["text"]


@mcp.tool()
async def write_file_tool(server_id: str, file_path: str, content: str) -> str:
    """Write content to a file on the remote server (creates or overwrites)."""
    result = await write_file({"server_id": server_id, "file_path": file_path, "content": content})
    return result[0]["text"]


# ── PM2 ───────────────────────────────────────────────────────────────────────

@mcp.tool()
async def pm2_manage_tool(server_id: str, action: str, app_name: str = "") -> str:
    """
    Manage PM2 processes on the remote server.
    Actions: list, start, stop, restart, delete, logs, status
    """
    result = await pm2_manage({"server_id": server_id, "action": action, "app_name": app_name})
    return result[0]["text"]


# ── Docker ────────────────────────────────────────────────────────────────────

@mcp.tool()
async def docker_manage_tool(
    server_id: str, action: str,
    name: str = "", image: str = "", command: str = "", lines: int = 50,
) -> str:
    """
    Manage Docker containers and images on the remote server.
    Actions: containers, running, start, stop, restart, remove, logs,
             inspect, exec, images, pull, rmi, stats, prune
    """
    result = await docker_manage({
        "server_id": server_id, "action": action,
        "name": name, "image": image, "command": command, "lines": lines,
    })
    return result[0]["text"]


@mcp.tool()
async def compose_manage_tool(
    server_id: str, action: str,
    path: str = ".", service: str = "", lines: int = 50,
) -> str:
    """
    Manage Docker Compose stacks on the remote server.
    Actions: up, down, restart, ps, logs, pull, build
    """
    result = await compose_manage({
        "server_id": server_id, "action": action,
        "path": path, "service": service, "lines": lines,
    })
    return result[0]["text"]


# ── Git & Deployments ─────────────────────────────────────────────────────────

@mcp.tool()
async def git_manage_tool(
    server_id: str, action: str,
    path: str = ".", branch: str = "", lines: int = 10,
) -> str:
    """
    Git operations on the remote server.
    Actions: status, pull, log, branch, checkout, diff, stash
    """
    result = await git_manage({
        "server_id": server_id, "action": action,
        "path": path, "branch": branch, "lines": lines,
    })
    return result[0]["text"]


@mcp.tool()
async def deploy_tool(
    server_id: str, path: str, branch: str = "main",
    script: str = "", service: str = "", pm2_app: str = "", compose_path: str = "",
) -> str:
    """
    Deploy code on the remote server.
    Auto-detects Node.js / Python. Runs: git pull → install → build → restart.
    Pass script= to use a custom deploy script.
    Restarts via: systemd service, PM2 app, or Docker Compose path.
    """
    result = await deploy({
        "server_id": server_id, "path": path, "branch": branch,
        "script": script, "service": service,
        "pm2_app": pm2_app, "compose_path": compose_path,
    })
    return result[0]["text"]


@mcp.tool()
async def rollback_tool(
    server_id: str, path: str, commits: int = 1,
    service: str = "", pm2_app: str = "",
) -> str:
    """Roll back N commits on the remote server and restart the service/app."""
    result = await rollback({
        "server_id": server_id, "path": path, "commits": commits,
        "service": service, "pm2_app": pm2_app,
    })
    return result[0]["text"]


@mcp.tool()
async def env_manage_tool(
    server_id: str, action: str,
    path: str = ".", key: str = "", value: str = "",
) -> str:
    """
    Manage .env files on the remote server (values redacted on read).
    Actions: read, list, write, delete
    """
    result = await env_manage({
        "server_id": server_id, "action": action,
        "path": path, "key": key, "value": value,
    })
    return result[0]["text"]


# ── Services & Processes ──────────────────────────────────────────────────────

@mcp.tool()
async def service_manage_tool(server_id: str, action: str, service: str = "") -> str:
    """
    Manage systemd services on the remote server.
    Actions: list, start, stop, restart, enable, disable, status, reload
    """
    result = await service_manage({"server_id": server_id, "action": action, "service": service})
    return result[0]["text"]


@mcp.tool()
async def port_check_tool(server_id: str, action: str = "open", port: str = "") -> str:
    """
    Check open ports and listeners on the remote server.
    Actions: open (all), check (specific port), connections
    """
    result = await port_check({"server_id": server_id, "action": action, "port": port})
    return result[0]["text"]


@mcp.tool()
async def process_manage_tool(
    server_id: str, action: str,
    name: str = "", pid: str = "", signal: str = "SIGTERM",
) -> str:
    """
    Manage OS-level processes on the remote server.
    Actions: list, top, find, kill
    """
    result = await process_manage({
        "server_id": server_id, "action": action,
        "name": name, "pid": pid, "signal": signal,
    })
    return result[0]["text"]


# ── Logs ──────────────────────────────────────────────────────────────────────

@mcp.tool()
async def log_manage_tool(
    server_id: str, action: str,
    path: str = "", pattern: str = "", service: str = "",
    container: str = "", lines: int = 50, since: str = "",
) -> str:
    """
    Monitor and analyze logs on the remote server.
    Actions: tail, search, errors, journal, docker, nginx, clear
    """
    result = await log_manage({
        "server_id": server_id, "action": action,
        "path": path, "pattern": pattern, "service": service,
        "container": container, "lines": lines, "since": since,
    })
    return result[0]["text"]


# ── Network & Health ──────────────────────────────────────────────────────────

@mcp.tool()
async def network_manage_tool(
    server_id: str, action: str,
    host: str = "", url: str = "", domain: str = "", count: int = 4,
) -> str:
    """
    Network diagnostics from the remote server.
    Actions: ping, curl, dns, ssl, traceroute, bandwidth, firewall
    """
    result = await network_manage({
        "server_id": server_id, "action": action,
        "host": host, "url": url, "domain": domain, "count": count,
    })
    return result[0]["text"]


@mcp.tool()
async def cron_manage_tool(
    server_id: str, action: str,
    user: str = "", job: str = "", pattern: str = "",
) -> str:
    """
    Manage cron jobs on the remote server.
    Actions: list, add, remove
    """
    result = await cron_manage({
        "server_id": server_id, "action": action,
        "user": user, "job": job, "pattern": pattern,
    })
    return result[0]["text"]


def run():
    mcp.run()


if __name__ == "__main__":
    run()
