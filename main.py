from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process
from tool import UclMcpTool

ucl_tool = UclMcpTool()

agent = Agent(
    role="Assistant",
    goal="Use MCP tools to help the user",
    backstory="Connected to Fastn UCL MCP.",
    tools=[ucl_tool],
    verbose=True,
    allow_delegation=False
)

task = Task(
    description="Create a Google doc titled Fastn UCL Test with content Hello from CrewAI MCP",
    expected_output="Document created",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print(crew.kickoff())
