"""
Tests for Server Tools
Simple tests to verify server connection management
"""

import pytest
from unittest.mock import patch, MagicMock
from src.tools.server_tools import list_servers, connect_server, connections
from src.config.settings import SERVERS


class TestServerTools:
    """Test suite for server management tools"""
    
    @pytest.mark.asyncio
    async def test_list_servers_empty(self):
        """Test listing servers when none are configured"""
        # Clear any existing server configurations
        SERVERS.clear()
        
        # Call list_servers
        result = await list_servers({})
        
        # Should return a message saying no servers configured
        assert len(result) == 1
        assert result[0]['type'] == 'text'
        assert 'No servers configured' in result[0]['text']
    
    @pytest.mark.asyncio
    @patch('src.tools.server_tools.SSHManager')
    async def test_connect_server_success(self, mock_ssh_manager):
        """Test successful server connection"""
        # Set up a fake server configuration
        SERVERS['test-server'] = {
            "host": "test.example.com",
            "port": 22,
            "username": "testuser",
            "password": "testpass",
            "key_file": None
        }
        
        # Clear any existing connections
        connections.clear()
        
        # Create a fake SSH manager
        mock_manager_instance = MagicMock()
        mock_ssh_manager.return_value = mock_manager_instance
        
        # Attempt to connect
        result = await connect_server({"server_id": "test-server"})
        
        # Verify connection was successful
        assert len(result) == 1
        assert 'Connected to test-server' in result[0]['text']
        assert 'test-server' in connections
        mock_manager_instance.connect.assert_called_once()