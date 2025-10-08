"""
PM2 process management tools
Handles Node.js application lifecycle management via PM2
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def pm2_manage(arguments: dict) -> List[dict]:
    """
    Manage PM2 processes on remote server
    
    Supported actions:
    - list: List all PM2 processes
    - status: Show status of specific app or all apps
    - start: Start an application
    - stop: Stop an application
    - restart: Restart an application
    - delete: Remove an application from PM2
    - logs: Show application logs
    
    Args:
        arguments: Dict containing:
            - server_id: Server identifier
            - action: PM2 action to perform
            - app_name: Application name (optional, required for most actions)
            
    Returns:
        List containing text response with PM2 output
        
    Raises:
        Exception: If server not found or app_name missing when required
    """
    server_id = arguments["server_id"]
    action = arguments["action"]
    app_name = arguments.get("app_name")
    
    # Auto-connect if not connected
    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")
    
    manager = connections[server_id]
    
    # Build PM2 command based on action
    if action == "list":
        result = manager.execute_command("pm2 jlist")
    elif action == "status":
        cmd = f"pm2 describe {app_name}" if app_name else "pm2 status"
        result = manager.execute_command(cmd)
    elif action == "logs":
        cmd = f"pm2 logs {app_name} --lines 50 --nostream" if app_name else "pm2 logs --lines 50 --nostream"
        result = manager.execute_command(cmd, timeout=60)
    else:
        # Actions requiring app_name: start, stop, restart, delete
        if not app_name:
            raise Exception(f"app_name required for action: {action}")
        result = manager.execute_command(f"pm2 {action} {app_name}")
    
    output = result['output'] if result['output'] else result['error']
    return [{"type": "text", "text": f"PM2 {action}:\n\n{output}"}]