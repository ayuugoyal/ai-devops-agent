"""
Network and health check tools
Monitor connectivity, SSL certs, and server health
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def health_check(arguments: dict) -> List[dict]:
    """
    Run a comprehensive health check on the remote server.

    Returns: uptime, load, memory, disk, top processes, listening ports,
             Docker status (if available), and failed systemd services.
    """
    server_id = arguments["server_id"]

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    checks = {
        "Uptime & Load":    "uptime",
        "Memory":           "free -h",
        "Disk":             "df -h --total | tail -5",
        "Top Processes":    "ps aux --sort=-%cpu | head -6",
        "Listening Ports":  "ss -tlnp 2>/dev/null | head -15",
        "Failed Services":  "systemctl list-units --failed --no-pager 2>/dev/null | head -10",
        "Docker":           "docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo 'Docker not available'",
    }

    sections = [f"=== Health Check: {server_id} ===\n"]
    for label, cmd in checks.items():
        res = mgr.execute_command(cmd)
        sections.append(f"── {label} ──\n{res['output'].strip() or res['error'].strip()}")

    return [{"type": "text", "text": "\n\n".join(sections)}]


async def network_manage(arguments: dict) -> List[dict]:
    """
    Network diagnostics and monitoring.

    Actions:
      ping      - ping a host from the remote server
      curl      - HTTP check a URL (status code + response time)
      dns       - DNS lookup
      ssl       - check SSL cert expiry for a domain
      traceroute - trace route to a host
      bandwidth  - quick bandwidth snapshot (rx/tx on main interface)
      firewall   - show iptables/ufw rules
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    host = arguments.get("host", "")
    url = arguments.get("url", "")
    domain = arguments.get("domain", "")
    count = arguments.get("count", 4)

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    if action == "ping":
        if not host:
            raise Exception("'host' required")
        cmd = f"ping -c {count} {host}"

    elif action == "curl":
        if not url:
            raise Exception("'url' required")
        cmd = f"curl -o /dev/null -s -w 'HTTP %{{http_code}} | Time: %{{time_total}}s | Size: %{{size_download}} bytes' '{url}'"

    elif action == "dns":
        if not host:
            raise Exception("'host' required")
        cmd = f"dig +short {host} || nslookup {host}"

    elif action == "ssl":
        if not domain:
            raise Exception("'domain' required")
        cmd = f"echo | openssl s_client -servername {domain} -connect {domain}:443 2>/dev/null | openssl x509 -noout -dates"

    elif action == "traceroute":
        if not host:
            raise Exception("'host' required")
        cmd = f"traceroute -m 15 {host} 2>/dev/null || tracepath {host}"

    elif action == "bandwidth":
        # Read /proc/net/dev for interface stats
        cmd = "cat /proc/net/dev | grep -v lo | awk 'NR>2 {print $1, \"RX:\", $2/1024/1024 \"MB\", \"TX:\", $10/1024/1024 \"MB\"}'"

    elif action == "firewall":
        cmd = "ufw status 2>/dev/null || iptables -L -n --line-numbers 2>/dev/null | head -30"

    else:
        raise Exception(f"Unknown network action: {action}")

    result = mgr.execute_command(cmd, timeout=30)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[network {action}]\n\n{output}"}]


async def cron_manage(arguments: dict) -> List[dict]:
    """
    Manage cron jobs on remote server.

    Actions: list, add, remove, enable, disable
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    user = arguments.get("user", "")
    job = arguments.get("job", "")      # full cron entry e.g. "*/5 * * * * /script.sh"
    pattern = arguments.get("pattern", "") # substring to match for remove

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    user_flag = f"-u {user}" if user else ""

    if action == "list":
        res = mgr.execute_command(f"crontab {user_flag} -l 2>/dev/null || echo 'No crontab'")
        return [{"type": "text", "text": f"[cron list]\n\n{res['output']}"}]

    elif action == "add":
        if not job:
            raise Exception("'job' required (e.g. '*/5 * * * * /path/script.sh')")
        cmd = f"(crontab {user_flag} -l 2>/dev/null; echo '{job}') | crontab {user_flag} -"
        mgr.execute_command(cmd)
        return [{"type": "text", "text": f"✓ Added cron job: {job}"}]

    elif action == "remove":
        if not pattern:
            raise Exception("'pattern' required to match the job to remove")
        cmd = f"crontab {user_flag} -l 2>/dev/null | grep -v '{pattern}' | crontab {user_flag} -"
        mgr.execute_command(cmd)
        return [{"type": "text", "text": f"✓ Removed cron job matching: {pattern}"}]

    else:
        raise Exception(f"Unknown cron action: {action}")
