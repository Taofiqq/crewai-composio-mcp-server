# workflow/github_workflow.py
"""
GitHub-only workflow using CrewAI
Sequential process: Fetch Issues → Fetch PRs → Analyze Data
"""

from crewai import Crew, Process
from agents.github_agent import github_agent
from tasks.github_tasks import (
    fetch_issues_task,
    fetch_pull_requests_task,
    analyze_github_data_task,
)
from config.settings import settings
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubWorkflow:
    """GitHub data fetching and analysis workflow"""

    def __init__(self):
        self.agent = github_agent
        self.tasks = self._setup_tasks()
        self.crew = self._create_crew()

    def _setup_tasks(self):
        """Setup tasks with proper context linking"""

        # Create fresh task instances
        issues_task = fetch_issues_task
        prs_task = fetch_pull_requests_task
        analysis_task = analyze_github_data_task

        # Set up context flow: analysis task uses outputs from previous tasks
        analysis_task.context = [issues_task, prs_task]

        return {"issues": issues_task, "prs": prs_task, "analysis": analysis_task}

    def _create_crew(self):
        """Create the CrewAI crew for GitHub workflow"""

        crew = Crew(
            agents=[self.agent],
            tasks=list(self.tasks.values()),
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
            memory=False,  # Keep it simple for now
            max_execution_time=600,  # 10 minutes total timeout
        )

        logger.info("✅ GitHub crew created with sequential process")
        return crew

    def execute(self):
        """Execute the GitHub workflow"""

        logger.info("🚀 Starting GitHub workflow execution...")
        logger.info(f"📂 Target repository: {settings.TARGET_REPOSITORY}")
        logger.info(f"🔍 Looking for '{settings.BUG_LABEL}' labels")

        start_time = datetime.now()

        try:
            # Execute the crew workflow
            result = self.crew.kickoff()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.info(f"✅ GitHub workflow completed in {execution_time:.2f} seconds")

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "repository": settings.TARGET_REPOSITORY,
                "timestamp": end_time.isoformat(),
            }

        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.error(
                f"❌ GitHub workflow failed after {execution_time:.2f} seconds: {e}"
            )

            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "repository": settings.TARGET_REPOSITORY,
                "timestamp": end_time.isoformat(),
            }

    def get_workflow_info(self):
        """Get information about the workflow setup"""

        return {
            "agent_role": self.agent.role,
            "total_tasks": len(self.tasks),
            "task_names": list(self.tasks.keys()),
            "process_type": "sequential",
            "target_repository": settings.TARGET_REPOSITORY,
            "bug_label": settings.BUG_LABEL,
        }


def run_github_workflow():
    """Convenience function to run the GitHub workflow"""

    workflow = GitHubWorkflow()

    # Log workflow info
    info = workflow.get_workflow_info()
    logger.info(f"📋 Workflow Info: {info}")

    # Execute workflow
    return workflow.execute()


# Create workflow instance for easy import
github_workflow = GitHubWorkflow()
