from setuptools import setup, find_packages


setup(
    name="mcp-remote-server",
    version="1.0.0",
    author="Ayush Goyal",
    author_email="ayushgoyal8178@gmail.com",
    description="MCP Server for Remote Server Management via SSH",
    url="https://github.com/ayuugoyal/mcp-remote-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "paramiko>=3.3.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-remote-server=src.server:main",
        ],
    },
)