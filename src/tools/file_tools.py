"""
File operation tools
Handles reading and listing files on remote servers
"""

from typing import List
from .server_tools import connections, connect_server, SERVERS


async def list_files(arguments: dict) -> List[dict]:
    """
    List files and directories in a remote path
    
    Args:
        arguments: Dict containing:
            - server_id: Server identifier
            - path: Directory path (default: current directory)
            
    Returns:
        List containing text response with file listing
        
    Raises:
        Exception: If server not found
    """
    server_id = arguments["server_id"]
    path = arguments.get("path", ".")
    
    # Auto-connect if not connected
    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")
    
    manager = connections[server_id]
    result = manager.execute_command(f"ls -lah {path}")
    
    return [{"type": "text", "text": f"Files in {path}:\n\n{result['output']}"}]


async def read_file(arguments: dict) -> List[dict]:
    """
    Read contents of a remote file
    
    Args:
        arguments: Dict containing:
            - server_id: Server identifier
            - file_path: Full path to the file
            
    Returns:
        List containing text response with file contents
        
    Raises:
        Exception: If server not found
    """
    server_id = arguments["server_id"]
    file_path = arguments["file_path"]
    
    # Auto-connect if not connected
    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")
    
    manager = connections[server_id]
    result = manager.execute_command(f"cat {file_path}")
    
    if result['exit_code'] != 0:
        return [{"type": "text", "text": f"Error: {result['error']}"}]
    
    return [{"type": "text", "text": f"Contents of {file_path}:\n\n{result['output']}"}]


async def write_file(arguments: dict) -> list:
    """Write content to a remote file (creates or overwrites)."""
    server_id = arguments["server_id"]
    file_path = arguments["file_path"]
    content = arguments["content"]

    if server_id not in connections:
        if server_id in SERVERS:
            await connect_server({"server_id": server_id})
        else:
            raise Exception(f"Server {server_id} not found")

    manager = connections[server_id]
    escaped = content.replace("'", "'\\''")
    result = manager.execute_command(f"cat > {file_path} << 'DEVOPS_EOF'\n{escaped}\nDEVOPS_EOF")
    if result["exit_code"] != 0:
        return [{"type": "text", "text": f"Error writing file: {result['error']}"}]
    return [{"type": "text", "text": f"✓ Written to {file_path}"}]
