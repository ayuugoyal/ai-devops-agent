"""
Docker management tools
Manage containers, images, volumes, and Docker Compose on remote servers
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def docker_manage(arguments: dict) -> List[dict]:
    """
    Full Docker lifecycle management on remote server.

    Actions:
      containers - list all containers (running + stopped)
      running    - list only running containers
      start      - start a container
      stop       - stop a container
      restart    - restart a container
      remove     - remove a stopped container
      logs       - tail container logs (last 50 lines)
      inspect    - inspect container details
      exec       - run a command inside a running container
      images     - list all local images
      pull       - pull an image from registry
      rmi        - remove an image
      stats      - live resource usage snapshot (one shot)
      prune      - remove all stopped containers + dangling images
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    name = arguments.get("name", "")
    image = arguments.get("image", "")
    command = arguments.get("command", "")
    lines = arguments.get("lines", 50)

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]

    cmd_map = {
        "containers": "docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'",
        "running":    "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'",
        "images":     "docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}'",
        "stats":      "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}'",
        "prune":      "docker system prune -f",
    }

    if action in cmd_map:
        result = mgr.execute_command(cmd_map[action])
    elif action == "start":
        result = mgr.execute_command(f"docker start {name}")
    elif action == "stop":
        result = mgr.execute_command(f"docker stop {name}")
    elif action == "restart":
        result = mgr.execute_command(f"docker restart {name}")
    elif action == "remove":
        result = mgr.execute_command(f"docker rm {name}")
    elif action == "logs":
        result = mgr.execute_command(f"docker logs --tail {lines} {name}")
    elif action == "inspect":
        result = mgr.execute_command(f"docker inspect {name}")
    elif action == "exec":
        if not command:
            raise Exception("'command' is required for exec action")
        result = mgr.execute_command(f"docker exec {name} {command}")
    elif action == "pull":
        if not image:
            raise Exception("'image' is required for pull action")
        result = mgr.execute_command(f"docker pull {image}", timeout=120)
    elif action == "rmi":
        if not image:
            raise Exception("'image' is required for rmi action")
        result = mgr.execute_command(f"docker rmi {image}")
    else:
        raise Exception(f"Unknown docker action: {action}")

    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[docker {action}]\n\n{output}"}]


async def compose_manage(arguments: dict) -> List[dict]:
    """
    Docker Compose lifecycle management.

    Actions: up, down, restart, ps, logs, pull, build
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    path = arguments.get("path", ".")
    service = arguments.get("service", "")
    lines = arguments.get("lines", 50)

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server '{server_id}' not found")

    mgr = connections[server_id]
    base = f"cd {path} && docker compose"

    if action == "up":
        cmd = f"{base} up -d {service}".strip()
    elif action == "down":
        cmd = f"{base} down"
    elif action == "restart":
        cmd = f"{base} restart {service}".strip()
    elif action == "ps":
        cmd = f"{base} ps"
    elif action == "logs":
        cmd = f"{base} logs --tail {lines} {service}".strip()
    elif action == "pull":
        cmd = f"{base} pull {service}".strip()
    elif action == "build":
        cmd = f"{base} build {service}".strip()
    else:
        raise Exception(f"Unknown compose action: {action}")

    result = mgr.execute_command(cmd, timeout=120)
    output = result["output"] or result["error"]
    return [{"type": "text", "text": f"[compose {action}]\n\n{output}"}]
