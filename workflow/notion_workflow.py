# workflow/notion_workflow.py
"""
Notion-only workflow using CrewAI
Sequential process: Search Pages → Create Database → Insert GitHub Data
"""

from crewai import Crew, Process
from agents.notion_agent import notion_agent
from tasks.notion_tasks import (
    search_parent_pages_task,
    create_github_database_task,
    insert_github_data_task,
)
from config.settings import settings
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotionWorkflow:
    """Notion database creation and data insertion workflow"""

    def __init__(self):
        self.agent = notion_agent
        self.tasks = self._setup_tasks()
        self.crew = self._create_crew()

    def _setup_tasks(self):
        """Setup tasks with proper context linking"""

        # Create fresh task instances
        search_task = search_parent_pages_task
        database_task = create_github_database_task
        insert_task = insert_github_data_task

        # Set up context flow: each task uses output from previous
        database_task.context = [search_task]
        insert_task.context = [search_task, database_task]

        return {"search": search_task, "database": database_task, "insert": insert_task}

    def _create_crew(self):
        """Create the CrewAI crew for Notion workflow"""

        crew = Crew(
            agents=[self.agent],
            tasks=list(self.tasks.values()),
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
            memory=False,  # Keep it simple for now
            max_execution_time=600,  # 10 minutes total timeout
        )

        logger.info("✅ Notion crew created with sequential process")
        return crew

    def execute_with_github_data(self, github_data: str):
        """Execute the Notion workflow with GitHub data as input"""

        logger.info("🚀 Starting Notion workflow execution...")
        logger.info(f"📂 Target repository: {settings.TARGET_REPOSITORY}")
        logger.info("📝 Creating GitHub Issues & PRs database in Notion")

        start_time = datetime.now()

        try:
            # Inject GitHub data into the insert task's description
            enriched_description = f"""
            {self.tasks['insert'].description}
            
            GitHub Data to Process:
            {github_data}
            """

            # Update the insert task with GitHub data
            self.tasks["insert"].description = enriched_description

            # Execute the crew workflow
            result = self.crew.kickoff()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.info(f"✅ Notion workflow completed in {execution_time:.2f} seconds")

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
                f"❌ Notion workflow failed after {execution_time:.2f} seconds: {e}"
            )

            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "repository": settings.TARGET_REPOSITORY,
                "timestamp": end_time.isoformat(),
            }

    def execute_standalone(self):
        """Execute Notion workflow with sample GitHub data for testing"""

        # Sample GitHub data for standalone testing
        sample_github_data = f"""
        GitHub Analysis Results from {settings.TARGET_REPOSITORY}:
        
        ISSUES FOUND:
        1. Issue #1070: "Chapter 15: Highlight error"
           - Labels: ['bug', 'frontend']
           - Assignees: ['johnsmith', 'janedoe']
           - State: open
           - Created: 2025-06-16
           - Repository: {settings.TARGET_REPOSITORY}
           
        2. Issue #1055: "Security vulnerability in auth"
           - Labels: ['bug', 'security', 'critical']
           - Assignees: ['securityteam']
           - State: open
           - Created: 2025-06-15
           - Repository: {settings.TARGET_REPOSITORY}
        
        PULL REQUESTS FOUND:
        1. PR #105: "Fix highlight bug in chapter 15"
           - Labels: ['bug', 'frontend']
           - Author: 'devlead'
           - Assignees: ['devlead']
           - State: open
           - Created: 2025-06-16
           - Repository: {settings.TARGET_REPOSITORY}
        
        SUMMARY:
        - Total items: 3 (2 issues, 1 PR)
        - Bug-labeled items: 3
        - Repository: {settings.TARGET_REPOSITORY}
        """

        return self.execute_with_github_data(sample_github_data)

    def get_workflow_info(self):
        """Get information about the workflow setup"""

        return {
            "agent_role": self.agent.role,
            "total_tasks": len(self.tasks),
            "task_names": list(self.tasks.keys()),
            "process_type": "sequential",
            "target_repository": settings.TARGET_REPOSITORY,
            "database_name": "GitHub Issues & PRs",
        }


def run_notion_workflow_standalone():
    """Convenience function to run the Notion workflow standalone"""

    workflow = NotionWorkflow()

    # Log workflow info
    info = workflow.get_workflow_info()
    logger.info(f"📋 Workflow Info: {info}")

    # Execute workflow with sample data
    return workflow.execute_standalone()


def run_notion_workflow_with_data(github_data: str):
    """Convenience function to run Notion workflow with provided GitHub data"""

    workflow = NotionWorkflow()
    return workflow.execute_with_github_data(github_data)


# Create workflow instance for easy import
notion_workflow = NotionWorkflow()
