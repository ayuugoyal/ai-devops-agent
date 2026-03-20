"""
Log monitoring and analysis tools
Tail, search, and analyze logs from files, journald, and Docker
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def log_manage(arguments: dict) -> List[dict]:
    """
    Monitor and analyze logs on remote server.

    Actions:
      tail      - tail a log file
      search    - grep a pattern in a log file
      errors    - filter ERROR/WARN lines from a log file
      journal   - query systemd journal (journalctl)
      docker    - fetch logs from a Docker container (alias for docker logs)
      nginx     - nginx access/error logs
      clear     - clear a log file
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    path = arguments.get("path", "")
    pattern = arguments.get("pattern", "")
    service = arguments.get("service", "")
    container = arguments.get("container", "")
    lines = arguments.get("lines", 50)
    since = arguments.get("since", "")        # e.g. "1h", "30m", "2024-01-01"

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    if action == "tail":
        if not path:
            raise Exception("'path' required for tail")
        cmd = f"tail -n {lines} {path}"

    elif action == "search":
        if not path or not pattern:
            raise Exception("'path' and 'pattern' required for search")
        cmd = f"grep -n '{pattern}' {path} | tail -n {lines}"

    elif action == "errors":
        if not path:
            raise Exception("'path' required for errors")
        cmd = f"grep -iE 'error|warn|exception|critical|fatal' {path} | tail -n {lines}"

    elif action == "journal":
        since_flag = f"--since '{since}'" if since else f"-n {lines}"
        service_flag = f"-u {service}" if service else ""
        cmd = f"journalctl {service_flag} {since_flag} --no-pager"

    elif action == "docker":
        if not container:
            raise Exception("'container' required for docker logs")
        cmd = f"docker logs --tail {lines} {container} 2>&1"

    elif action == "nginx":
        log_type = arguments.get("log_type", "access")
        log_path = f"/var/log/nginx/{log_type}.log"
        if pattern:
            cmd = f"grep '{pattern}' {log_path} | tail -n {lines}"
        else:
            cmd = f"tail -n {lines} {log_path}"

    elif action == "clear":
        if not path:
            raise Exception("'path' required for clear")
        cmd = f"truncate -s 0 {path} && echo 'Cleared: {path}'"

    else:
        raise Exception(f"Unknown log action: {action}")

    result = mgr.execute_command(cmd, timeout=30)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[log {action}]\n\n{output}"}]
