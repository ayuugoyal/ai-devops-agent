"""
MCP Server for Remote Server Management
Main entry point for the MCP protocol server
"""

import asyncio
import json
import sys
from typing import Optional, Dict, Any

from .config.settings import load_servers_from_env
from .tools import (
    list_servers,
    connect_server,
    disconnect_server,
    pm2_manage,
    list_files,
    read_file,
    system_info,
    run_command
)
from .tools.server_tools import connections


async def handle_request(request: dict) -> Optional[dict]:
    """
    Handle incoming MCP protocol requests
    
    Processes three main request types:
    - initialize: Protocol handshake
    - tools/list: List available tools
    - tools/call: Execute a tool
    
    Args:
        request: JSON-RPC 2.0 request object
        
    Returns:
        JSON-RPC 2.0 response object or None for notifications
    """
    method = request.get("method")
    request_id = request.get("id")
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "remote-server-mcp",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "list_servers",
                            "description": "List all configured servers from environment",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        },
                        {
                            "name": "connect_server",
                            "description": "Connect to a configured remote server",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID from configuration"
                                    }
                                },
                                "required": ["server_id"]
                            }
                        },
                        {
                            "name": "pm2_manage",
                            "description": "Manage PM2 processes (list, start, stop, restart, delete, logs, status)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    },
                                    "action": {
                                        "type": "string",
                                        "enum": ["list", "start", "stop", "restart", "delete", "logs", "status"],
                                        "description": "Action to perform"
                                    },
                                    "app_name": {
                                        "type": "string",
                                        "description": "App name (required for most actions)"
                                    }
                                },
                                "required": ["server_id", "action"]
                            }
                        },
                        {
                            "name": "list_files",
                            "description": "List files and directories in a path",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": "Directory path (default: current directory)"
                                    }
                                },
                                "required": ["server_id"]
                            }
                        },
                        {
                            "name": "read_file",
                            "description": "Read the contents of a file",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    },
                                    "file_path": {
                                        "type": "string",
                                        "description": "Full path to the file"
                                    }
                                },
                                "required": ["server_id", "file_path"]
                            }
                        },
                        {
                            "name": "system_info",
                            "description": "Get system information (CPU, memory, disk usage)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    }
                                },
                                "required": ["server_id"]
                            }
                        },
                        {
                            "name": "run_command",
                            "description": "Run any custom shell command on the remote server",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    },
                                    "command": {
                                        "type": "string",
                                        "description": "Shell command to execute"
                                    }
                                },
                                "required": ["server_id", "command"]
                            }
                        },
                        {
                            "name": "disconnect_server",
                            "description": "Disconnect from a remote server",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "server_id": {
                                        "type": "string",
                                        "description": "Server ID"
                                    }
                                },
                                "required": ["server_id"]
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Map tool names to functions
            tools = {
                "list_servers": list_servers,
                "connect_server": connect_server,
                "pm2_manage": pm2_manage,
                "list_files": list_files,
                "read_file": read_file,
                "system_info": system_info,
                "run_command": run_command,
                "disconnect_server": disconnect_server
            }
            
            if tool_name in tools:
                try:
                    result = await tools[tool_name](arguments)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": result
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                            "isError": True
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        elif method == "notifications/initialized":
            # Notifications don't require responses
            return None
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    except Exception as e:
        print(f"Error handling request: {str(e)}", file=sys.stderr)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


async def main():
    """
    Main MCP server loop
    
    Implements stdio-based JSON-RPC 2.0 communication:
    1. Reads JSON requests from stdin (one per line)
    2. Processes requests through handle_request()
    3. Writes JSON responses to stdout
    """
    load_servers_from_env()
    
    print("Remote Server MCP ready", file=sys.stderr)
    
    while True:
        try:
            # Read request from stdin
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            # Parse and handle request
            request = json.loads(line)
            print(f"Received request: {request.get('method')}", file=sys.stderr)
            
            response = await handle_request(request)
            
            # Send response (if not a notification)
            if response:
                print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)


def run():
    """Entry point for console script"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr)
        # Clean up connections
        for server_id in list(connections.keys()):
            connections[server_id].close()


if __name__ == "__main__":
    run()
