# Fastn × CrewAI MCP Example

This repository demonstrates integrating Fastn UCL MCP with the CrewAI Python SDK.

It shows how CrewAI agents can dynamically discover and invoke tools exposed by Fastn MCP using MCPServerAdapter.

## ⚠️ Important
This project uses the CrewAI Python SDK.



## What This Includes
	•	Dynamic MCP tool discovery
	•	CrewAI agent + task orchestration
	•	MCP proxy tool (tool.py)
	•	Minimal runnable example (main.py)
	•	Interactive CLI assistant (cli_full.py)

## Requirements
	•	Python 3.10+
	•	Running Fastn MCP server
	•	OpenAI API key

## Setup

1. Create virtual environment

python -m venv venv
source venv/bin/activate

2. Install dependencies

pip install -r requirements.txt

3. Configure environment

cp .env.example .env

Edit .env:

OPENAI_API_KEY=your_key_here
MCP_SERVER_URL=http://localhost:3001

