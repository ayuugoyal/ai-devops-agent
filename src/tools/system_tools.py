"""
System monitoring and command execution tools
Provides system information and custom command execution
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def system_info(arguments: dict) -> List[dict]:
    """
    Get comprehensive system information from remote server
    
    Retrieves:
    - System uptime
    - CPU usage
    - Memory usage
    - Disk usage
    
    Args:
        arguments: Dict containing server_id
        
    Returns:
        List containing text response with system information
        
    Raises:
        Exception: If server not found
    """
    server_id = arguments["server_id"]
    
    # Auto-connect if not connected
    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")
    
    manager = connections[server_id]
    
    commands = {
        "uptime": "uptime",
        "memory": "free -h",
        "disk": "df -h",
        "cpu": "top -bn1 | grep 'Cpu(s)'",
    }
    
    info = {}
    for key, cmd in commands.items():
        result = manager.execute_command(cmd)
        info[key] = result['output'].strip()
    
    output = f"""System Information for {server_id}:

Uptime: {info['uptime']}

CPU: {info['cpu']}

Memory:
{info['memory']}

Disk:
{info['disk']}"""
    
    return [{"type": "text", "text": output}]


async def run_command(arguments: dict) -> List[dict]:
    """
    Execute custom shell command on remote server
    
    Provides full flexibility to run any shell command
    Use with caution - ensure proper security measures
    
    Args:
        arguments: Dict containing:
            - server_id: Server identifier
            - command: Shell command to execute
            
    Returns:
        List containing text response with command output
        
    Raises:
        Exception: If server not found
    """
    server_id = arguments["server_id"]
    command = arguments["command"]
    
    # Auto-connect if not connected
    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")
    
    manager = connections[server_id]
    result = manager.execute_command(command)
    
    output = f"Command: {command}\n\n"
    if result['output']:
        output += f"Output:\n{result['output']}\n"
    if result['error']:
        output += f"Error:\n{result['error']}\n"
    output += f"\nExit code: {result['exit_code']}"
    
    return [{"type": "text", "text": output}]
