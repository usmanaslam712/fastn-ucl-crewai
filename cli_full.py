# FULL CLI MCP + CrewAI integration
# (condensed version of what you shared)

import os, sys, uuid, json, time, warnings, logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter

load_dotenv()
warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

class MCPCrewAIIntegration:

    def __init__(self, server_url):
        self.server_url = server_url
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.session_id = str(uuid.uuid4())[:8]
        self.chat_history = []
        self.chat_dir = Path("chat_history")
        self.chat_dir.mkdir(exist_ok=True)

    def get_llm(self):
        return LLM(model="gpt-4.1", api_key=self.openai_api_key)

    def get_server_params(self):
        return {"url": self.server_url, "transport": "streamable-http"}

    def connect(self):
        with MCPServerAdapter(self.get_server_params()) as tools:
            self.tools = list(tools)
            return bool(self.tools)

    def create_agent(self):
        return Agent(
            role="Assistant",
            goal="Help users via MCP",
            backstory="Fastn UCL MCP powered",
            tools=self.tools,
            llm=self.get_llm(),
            verbose=False,
            allow_delegation=False
        )

    def execute(self, prompt):
        agent = self.create_agent()
        task = Task(description=prompt, agent=agent)
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
        return crew.kickoff()

def main():
    url = os.getenv("MCP_SERVER_URL")
    app = MCPCrewAIIntegration(url)
    if not app.connect():
        print("No MCP tools found")
        return

    while True:
        q = input("Ask> ")
        if q in ["exit","quit"]:
            break
        print(app.execute(q))

if __name__ == "__main__":
    main()
