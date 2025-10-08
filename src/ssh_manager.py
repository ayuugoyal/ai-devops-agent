"""
SSH Connection Manager
Handles SSH connections to remote servers using paramiko
"""

import os
from typing import Dict, Optional
import paramiko


class SSHManager:
    """
    Manages SSH connections to remote servers
    
    Supports both password and SSH key authentication
    """
    
    def __init__(self, config: dict):
        """
        Initialize SSH Manager
        
        Args:
            config: Dictionary containing connection parameters
                   (host, port, username, password/key_file)
        """
        self.config = config
        self.client: Optional[paramiko.SSHClient] = None
    
    def connect(self) -> bool:
        """
        Establish SSH connection to the remote server
        
        Returns:
            bool: True if connection successful
            
        Raises:
            Exception: If connection fails
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.config.get("key_file"):
                key_path = os.path.expanduser(self.config["key_file"])
                self.client.connect(
                    hostname=self.config["host"],
                    port=self.config["port"],
                    username=self.config["username"],
                    key_filename=key_path,
                    timeout=10
                )
            else:
                self.client.connect(
                    hostname=self.config["host"],
                    port=self.config["port"],
                    username=self.config["username"],
                    password=self.config["password"],
                    timeout=10
                )
            return True
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, any]:
        """
        Execute a shell command on the remote server
        
        Args:
            command: Shell command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Dict containing output, error, and exit_code
        """
        if not self.client:
            raise Exception("Not connected to server")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                "output": output,
                "error": error,
                "exit_code": exit_code
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"Command execution error: {str(e)}",
                "exit_code": -1
            }
    
    def close(self):
        """Close the SSH connection"""
        if self.client:
            self.client.close()
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()