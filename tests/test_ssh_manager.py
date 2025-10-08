"""
Tests for SSH Manager
Simple tests to verify SSH connection and command execution
"""

import pytest
from unittest.mock import patch, MagicMock
from src.ssh_manager import SSHManager


class TestSSHManager:
    """Test suite for SSHManager class"""
    
    @patch('src.ssh_manager.paramiko.SSHClient')
    def test_connect_with_password(self, mock_ssh_class):
        """Test successful connection with password authentication"""
        # Create a fake SSH client
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client
        
        # Sample server configuration
        config = {
            "host": "test.example.com",
            "port": 22,
            "username": "testuser",
            "password": "testpass",
            "key_file": None
        }
        
        # Create manager and connect
        manager = SSHManager(config)
        result = manager.connect()
        
        # Verify connection was successful
        assert result is True
        assert manager.client is not None
        mock_client.connect.assert_called_once()
    
    @patch('src.ssh_manager.paramiko.SSHClient')
    def test_execute_command_success(self, mock_ssh_class):
        """Test successful command execution"""
        # Create fake SSH client and command outputs
        mock_client = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdin = MagicMock()
        
        # Simulate command returning "Hello World"
        mock_stdout.read.return_value = b"Hello World"
        mock_stderr.read.return_value = b""
        mock_stdout.channel.recv_exit_status.return_value = 0
        
        mock_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)
        mock_ssh_class.return_value = mock_client
        
        # Create manager, connect, and run command
        config = {
            "host": "test.example.com",
            "port": 22,
            "username": "testuser",
            "password": "testpass",
            "key_file": None
        }
        
        manager = SSHManager(config)
        manager.connect()
        result = manager.execute_command("echo 'Hello World'")
        
        # Verify command executed successfully
        assert result['output'] == "Hello World"
        assert result['error'] == ""
        assert result['exit_code'] == 0
