"""
Deployment and Git tools
Handle code deployments, rollbacks, and environment management
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def git_manage(arguments: dict) -> List[dict]:
    """
    Git operations on remote server.

    Actions: status, pull, log, branch, checkout, diff, stash
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    path = arguments.get("path", ".")
    branch = arguments.get("branch", "")
    lines = arguments.get("lines", 10)

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    base = f"cd {path} && git"

    if action == "status":
        cmd = f"{base} status"
    elif action == "pull":
        cmd = f"{base} pull"
    elif action == "log":
        cmd = f"{base} log --oneline -{lines}"
    elif action == "branch":
        cmd = f"{base} branch -a"
    elif action == "checkout":
        if not branch:
            raise Exception("'branch' required for checkout")
        cmd = f"{base} checkout {branch}"
    elif action == "diff":
        cmd = f"{base} diff --stat HEAD~1"
    elif action == "stash":
        cmd = f"{base} stash"
    else:
        raise Exception(f"Unknown git action: {action}")

    result = mgr.execute_command(cmd, timeout=60)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[git {action}] @ {path}\n\n{output}"}]


async def deploy(arguments: dict) -> List[dict]:
    """
    Run a deployment on the remote server.

    Performs: git pull → install deps → build → restart service
    Configurable per step, supports custom deploy scripts.
    """
    server_id = arguments["server_id"]
    path = arguments.get("path", ".")
    branch = arguments.get("branch", "main")
    script = arguments.get("script", "")          # custom deploy script path
    service = arguments.get("service", "")        # systemd service to restart after deploy
    pm2_app = arguments.get("pm2_app", "")        # PM2 app to restart after deploy
    compose_path = arguments.get("compose_path", "") # docker-compose path to restart

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    steps = []
    results = []

    if script:
        steps.append(("Running deploy script", f"cd {path} && bash {script}"))
    else:
        steps.append(("Git pull", f"cd {path} && git fetch origin && git checkout {branch} && git pull origin {branch}"))

        # Auto-detect package manager and install
        detect = mgr.execute_command(f"ls {path}")
        if "package.json" in detect["output"]:
            pkg = mgr.execute_command(f"ls {path} | grep -E 'pnpm-lock|yarn.lock|package-lock'")
            if "pnpm-lock" in pkg["output"]:
                steps.append(("Install deps (pnpm)", f"cd {path} && pnpm install --frozen-lockfile"))
            elif "yarn.lock" in pkg["output"]:
                steps.append(("Install deps (yarn)", f"cd {path} && yarn install --frozen-lockfile"))
            else:
                steps.append(("Install deps (npm)", f"cd {path} && npm ci"))

            # Check for build script
            has_build = mgr.execute_command(f"cd {path} && node -e \"const p=require('./package.json');process.exit(p.scripts&&p.scripts.build?0:1)\" 2>/dev/null; echo $?")
            if "0" in has_build["output"]:
                steps.append(("Build", f"cd {path} && npm run build"))

        elif "requirements.txt" in detect["output"]:
            steps.append(("Install deps (pip)", f"cd {path} && pip install -r requirements.txt -q"))

    # Restart target
    if pm2_app:
        steps.append(("Restart PM2", f"pm2 restart {pm2_app}"))
    elif service:
        steps.append(("Restart service", f"sudo systemctl restart {service}"))
    elif compose_path:
        steps.append(("Compose up", f"cd {compose_path} && docker compose up -d"))

    for step_name, cmd in steps:
        res = mgr.execute_command(cmd, timeout=180)
        status = "✓" if res["exit_code"] == 0 else "✗"
        results.append(f"{status} {step_name}\n{res['output'] or res['error']}")

    return [{"type": "text", "text": f"Deployment @ {path}\n{'='*50}\n\n" + "\n\n".join(results)}]


async def rollback(arguments: dict) -> List[dict]:
    """
    Roll back to a previous git commit on the remote server.
    Optionally restarts a service/PM2 app after rollback.
    """
    server_id = arguments["server_id"]
    path = arguments.get("path", ".")
    commits = arguments.get("commits", 1)
    service = arguments.get("service", "")
    pm2_app = arguments.get("pm2_app", "")

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    results = []

    res = mgr.execute_command(f"cd {path} && git reset --hard HEAD~{commits}")
    results.append(f"✓ Rolled back {commits} commit(s)\n{res['output']}")

    if pm2_app:
        res2 = mgr.execute_command(f"pm2 restart {pm2_app}")
        results.append(f"✓ Restarted PM2: {pm2_app}\n{res2['output']}")
    elif service:
        res2 = mgr.execute_command(f"sudo systemctl restart {service}")
        results.append(f"✓ Restarted service: {service}\n{res2['output']}")

    return [{"type": "text", "text": "\n\n".join(results)}]


async def env_manage(arguments: dict) -> List[dict]:
    """
    Manage environment files on remote server.

    Actions:
      read   - read .env file (redacts secrets)
      write  - write a key=value pair into .env
      delete - remove a key from .env
      list   - list all keys (values redacted)
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    path = arguments.get("path", ".")
    key = arguments.get("key", "")
    value = arguments.get("value", "")

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    env_file = f"{path}/.env"

    if action in ("read", "list"):
        res = mgr.execute_command(f"cat {env_file} 2>/dev/null || echo 'No .env file found'")
        # Redact values for security
        lines = []
        for line in res["output"].splitlines():
            if "=" in line and not line.startswith("#"):
                k, _ = line.split("=", 1)
                lines.append(f"{k}=***")
            else:
                lines.append(line)
        return [{"type": "text", "text": f"[.env @ {path}] (values redacted)\n\n" + "\n".join(lines)}]

    elif action == "write":
        if not key:
            raise Exception("'key' required for write action")
        # Remove existing key then append
        cmd = f"sed -i '/^{key}=/d' {env_file} 2>/dev/null; echo '{key}={value}' >> {env_file}"
        mgr.execute_command(cmd)
        return [{"type": "text", "text": f"✓ Set {key} in {env_file}"}]

    elif action == "delete":
        if not key:
            raise Exception("'key' required for delete action")
        mgr.execute_command(f"sed -i '/^{key}=/d' {env_file}")
        return [{"type": "text", "text": f"✓ Removed {key} from {env_file}"}]

    else:
        raise Exception(f"Unknown env action: {action}")
