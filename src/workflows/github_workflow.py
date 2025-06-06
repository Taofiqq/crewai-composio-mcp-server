from crewai import Crew, Process
from src.agents.github_analyzer import GitHubAnalyzer
from src.agents.notion_writer import NotionWriter
from src.agents.calendar_scheduler import CalendarScheduler
from src.tasks.github_analysis_task import create_github_analysis_task
from src.tasks.notion_documentation_task import create_notion_documentation_task
from src.tasks.calendar_scheduling_task import create_calendar_scheduling_task
from config.settings import *


class GitHubWorkflow:
    def __init__(self):
        # Initialize agents
        self.github_analyzer = GitHubAnalyzer().get_agent()
        self.notion_writer = NotionWriter().get_agent()
        self.calendar_scheduler = CalendarScheduler().get_agent()

        # Create tasks
        self.github_task = create_github_analysis_task(self.github_analyzer)
        self.notion_task = create_notion_documentation_task(self.notion_writer)
        self.calendar_task = create_calendar_scheduling_task(self.calendar_scheduler)

        # Set up task dependencies
        self.notion_task.context = [
            self.github_task
        ]  # Notion depends on GitHub analysis
        self.calendar_task.context = [
            self.github_task,
            self.notion_task,
        ]  # Calendar depends on both

        # Create the crew
        self.crew = self._create_crew()

    def _create_crew(self):
        """Create and configure the crew"""
        return Crew(
            agents=[self.github_analyzer, self.notion_writer, self.calendar_scheduler],
            tasks=[self.github_task, self.notion_task, self.calendar_task],
            process=Process.sequential,  # Execute tasks in order
            memory=True,  # Enable memory sharing between agents
            verbose=VERBOSE_MODE,
            max_rpm=30,  # Rate limiting
        )

    def execute(self, repo_url: str, issue_number: str):
        """Execute the complete workflow"""
        try:
            print(f"🚀 Starting GitHub workflow for {repo_url}/issues/{issue_number}")

            # Input data for the workflow
            inputs = {"repo_url": repo_url, "issue_number": issue_number}

            # Execute the crew
            result = self.crew.kickoff(inputs=inputs)

            print("✅ Workflow completed successfully!")
            return result

        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            raise e

    def get_crew_info(self):
        """Get information about the crew"""
        return {
            "agents": len(self.crew.agents),
            "tasks": len(self.crew.tasks),
            "process": self.crew.process,
            "memory_enabled": self.crew.memory,
        }
