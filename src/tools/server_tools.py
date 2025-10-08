"""
Server connection management tools
Handles listing, connecting, and disconnecting from servers
"""

from typing import Dict, List
from ..config.settings import SERVERS
from ..ssh_manager import SSHManager

# Store active connections
connections: Dict[str, SSHManager] = {}


async def list_servers(arguments: dict) -> List[dict]:
    """
    List all configured servers with their connection status
    
    Args:
        arguments: Empty dict (no arguments required)
        
    Returns:
        List containing text response with server information
    """
    if not SERVERS:
        return [{
            "type": "text",
            "text": "No servers configured. Please set environment variables."
        }]
    
    output = "Configured Servers:\n\n"
    for server_id, config in SERVERS.items():
        auth = "SSH Key" if config.get("key_file") else "Password"
        status = "🟢 Connected" if server_id in connections else "⚪ Disconnected"
        output += f"• {server_id}: {config['username']}@{config['host']}:{config['port']} ({auth}) {status}\n"
    
    return [{"type": "text", "text": output}]


async def connect_server(arguments: dict) -> List[dict]:
    """
    Establish SSH connection to a configured server
    
    Args:
        arguments: Dict containing server_id
        
    Returns:
        List containing text response with connection status
        
    Raises:
        Exception: If server not found or connection fails
    """
    server_id = arguments["server_id"]
    
    if server_id not in SERVERS:
        available = ", ".join(SERVERS.keys())
        raise Exception(f"Server '{server_id}' not found. Available: {available}")
    
    if server_id in connections:
        return [{"type": "text", "text": f"Already connected to {server_id}"}]
    
    config = SERVERS[server_id]
    manager = SSHManager(config)
    manager.connect()
    connections[server_id] = manager
    
    auth_method = "SSH key" if config.get("key_file") else "password"
    return [{
        "type": "text",
        "text": f"✓ Connected to {server_id} ({config['username']}@{config['host']}) using {auth_method}"
    }]


async def disconnect_server(arguments: dict) -> List[dict]:
    """
    Close SSH connection to a server
    
    Args:
        arguments: Dict containing server_id
        
    Returns:
        List containing text response with disconnection status
    """
    server_id = arguments["server_id"]
    
    if server_id in connections:
        connections[server_id].close()
        del connections[server_id]
        return [{"type": "text", "text": f"✓ Disconnected from {server_id}"}]
    
    return [{"type": "text", "text": f"Server {server_id} was not connected"}]


def get_connection(server_id: str) -> SSHManager:
    """
    Get existing connection or raise exception
    
    Args:
        server_id: Server identifier
        
    Returns:
        SSHManager instance
        
    Raises:
        Exception: If not connected or server not found
    """
    if server_id not in connections:
        raise Exception(f"Not connected to {server_id}. Please connect first.")
    return connections[server_id]

