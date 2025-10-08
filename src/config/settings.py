"""
Configuration and settings management
Loads server configurations from environment variables
"""

import os
import sys
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Store server configurations
SERVERS: Dict[str, dict] = {}


def load_servers_from_env() -> Dict[str, dict]:
    """
    Load server configurations from environment variables
    
    Supports multiple servers with format:
    - SERVER_N_ID, SERVER_N_HOST, SERVER_N_PORT, etc.
    - Legacy single server format: SERVER_ID, SERVER_HOST, etc.
    
    Returns:
        Dict[str, dict]: Dictionary of server configurations
    """
    global SERVERS
    SERVERS.clear()
    
    i = 1
    while True:
        host = os.getenv(f"SERVER_{i}_HOST")
        if not host:
            if i == 1:
                host = os.getenv("SERVER_HOST")
            if not host:
                break
        
        server_id = os.getenv(f"SERVER_{i}_ID", f"server_{i}")
        if i == 1 and not os.getenv(f"SERVER_{i}_HOST"):
            server_id = os.getenv("SERVER_ID", "default")
        
        config = {
            "host": host,
            "port": int(os.getenv(f"SERVER_{i}_PORT", os.getenv("SERVER_PORT", "22"))),
            "username": os.getenv(f"SERVER_{i}_USER", os.getenv("SERVER_USER", "root")),
            "password": os.getenv(f"SERVER_{i}_PASSWORD", os.getenv("SERVER_PASSWORD")),
            "key_file": os.getenv(f"SERVER_{i}_KEY_FILE", os.getenv("SERVER_KEY_FILE"))
        }
        
        SERVERS[server_id] = config
        i += 1
    
    print(f"Loaded {len(SERVERS)} server(s) from environment", file=sys.stderr)
    for sid in SERVERS:
        print(f"  - {sid}: {SERVERS[sid]['username']}@{SERVERS[sid]['host']}", file=sys.stderr)
    
    return SERVERS