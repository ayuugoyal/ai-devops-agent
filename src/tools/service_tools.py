"""
System service management tools
Control systemd services, check ports, and manage processes
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def service_manage(arguments: dict) -> List[dict]:
    """
    Manage systemd services on remote server.

    Actions: start, stop, restart, status, enable, disable, list, reload
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    service = arguments.get("service", "")

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    if action == "list":
        cmd = "systemctl list-units --type=service --state=running --no-pager"
    elif action in ("start", "stop", "restart", "enable", "disable", "reload"):
        if not service:
            raise Exception(f"'service' name required for action: {action}")
        cmd = f"sudo systemctl {action} {service}"
    elif action == "status":
        cmd = f"sudo systemctl status {service} --no-pager" if service else \
              "systemctl list-units --type=service --no-pager | head -40"
    else:
        raise Exception(f"Unknown service action: {action}")

    result = mgr.execute_command(cmd)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[service {action}] {service}\n\n{output}"}]


async def port_check(arguments: dict) -> List[dict]:
    """
    Check open ports and network listeners on remote server.

    Actions: open (all open ports), check (specific port), connections (active connections)
    """
    server_id = arguments["server_id"]
    action = arguments.get("action", "open")
    port = arguments.get("port", "")

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    if action == "open":
        cmd = "ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null"
    elif action == "check":
        if not port:
            raise Exception("'port' required for check action")
        cmd = f"ss -tlnp | grep :{port} || echo 'Port {port} not listening'"
    elif action == "connections":
        cmd = "ss -tnp | head -30"
    else:
        raise Exception(f"Unknown port_check action: {action}")

    result = mgr.execute_command(cmd)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[port {action}]\n\n{output}"}]


async def process_manage(arguments: dict) -> List[dict]:
    """
    Manage OS-level processes.

    Actions: list (top processes), find (by name), kill (by PID or name), top
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    name = arguments.get("name", "")
    pid = arguments.get("pid", "")
    signal = arguments.get("signal", "SIGTERM")

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    if action == "list":
        cmd = "ps aux --sort=-%cpu | head -20"
    elif action == "top":
        cmd = "top -bn1 | head -25"
    elif action == "find":
        if not name:
            raise Exception("'name' required for find action")
        cmd = f"pgrep -a {name} 2>/dev/null || ps aux | grep {name} | grep -v grep"
    elif action == "kill":
        if pid:
            cmd = f"kill -{signal} {pid}"
        elif name:
            cmd = f"pkill -{signal} {name}"
        else:
            raise Exception("Either 'pid' or 'name' required for kill action")
    else:
        raise Exception(f"Unknown process action: {action}")

    result = mgr.execute_command(cmd)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[process {action}]\n\n{output}"}]
