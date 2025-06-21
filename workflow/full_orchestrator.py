# # workflow/orchestrator.py
# """
# Combined GitHub + Notion workflow orchestrator
# Sequential process: GitHub Data Fetching → Notion Database Management
# """

# from crewai import Crew, Process
# from agents.github_agent import github_agent
# from agents.notion_agent import notion_agent
# from tasks.github_tasks import (
#     fetch_issues_task,
#     fetch_pull_requests_task,
#     analyze_github_data_task,
# )
# from tasks.notion_tasks import (
#     search_parent_pages_task,
#     create_github_database_task,
#     insert_github_data_task,
# )
# from config.settings import settings
# import logging
# from datetime import datetime

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# class GitHubNotionOrchestrator:
#     """Combined GitHub + Notion workflow orchestrator"""

#     def __init__(self):
#         self.github_agent = github_agent
#         self.notion_agent = notion_agent
#         self.tasks = self._setup_tasks()
#         self.crew = self._create_crew()

#     def _setup_tasks(self):
#         """Setup tasks with proper context linking for data flow"""

#         # GitHub tasks (from github_tasks.py)
#         github_issues_task = fetch_issues_task
#         github_prs_task = fetch_pull_requests_task
#         github_analysis_task = analyze_github_data_task

#         # Notion tasks (from notion_tasks.py)
#         notion_search_task = search_parent_pages_task
#         notion_database_task = create_github_database_task
#         notion_insert_task = insert_github_data_task

#         # Set up GitHub task context flow
#         github_analysis_task.context = [github_issues_task, github_prs_task]

#         # Set up Notion task context flow
#         notion_database_task.context = [notion_search_task]

#         # CRITICAL: Notion insert task gets GitHub data
#         notion_insert_task.context = [
#             notion_search_task,  # For database ID
#             notion_database_task,  # For database creation confirmation
#             github_issues_task,  # For GitHub issues data
#             github_prs_task,  # For GitHub PRs data
#             github_analysis_task,  # For GitHub analysis results
#         ]

#         return {
#             # GitHub workflow
#             "github_issues": github_issues_task,
#             "github_prs": github_prs_task,
#             "github_analysis": github_analysis_task,
#             # Notion workflow
#             "notion_search": notion_search_task,
#             "notion_database": notion_database_task,
#             "notion_insert": notion_insert_task,
#         }

#     def _create_crew(self):
#         """Create the CrewAI crew for combined workflow"""

#         crew = Crew(
#             agents=[self.github_agent, self.notion_agent],
#             tasks=list(self.tasks.values()),
#             process=Process.sequential,  # Execute tasks in order
#             verbose=True,
#             memory=False,  # Keep it simple for now
#             max_execution_time=900,  # 15 minutes total timeout
#         )

#         logger.info("✅ Combined GitHub + Notion crew created with sequential process")
#         return crew

#     def execute(self, repository: str = None):
#         """Execute the combined GitHub + Notion workflow"""

#         target_repo = repository or settings.TARGET_REPOSITORY

#         logger.info("🚀 Starting Combined GitHub + Notion workflow execution...")
#         logger.info(f"📂 Target repository: {target_repo}")
#         logger.info("🔄 Flow: GitHub Data → Notion Database")

#         start_time = datetime.now()

#         try:
#             # Update GitHub tasks with target repository
#             self._update_github_tasks_repository(target_repo)

#             # Execute the crew workflow
#             result = self.crew.kickoff()

#             end_time = datetime.now()
#             execution_time = (end_time - start_time).total_seconds()

#             logger.info(
#                 f"✅ Combined workflow completed in {execution_time:.2f} seconds"
#             )

#             return {
#                 "success": True,
#                 "result": result,
#                 "execution_time": execution_time,
#                 "repository": target_repo,
#                 "github_agent": "completed",
#                 "notion_agent": "completed",
#                 "database_created": True,
#                 "timestamp": end_time.isoformat(),
#             }

#         except Exception as e:
#             end_time = datetime.now()
#             execution_time = (end_time - start_time).total_seconds()

#             logger.error(
#                 f"❌ Combined workflow failed after {execution_time:.2f} seconds: {e}"
#             )

#             return {
#                 "success": False,
#                 "error": str(e),
#                 "execution_time": execution_time,
#                 "repository": target_repo,
#                 "github_agent": "unknown",
#                 "notion_agent": "unknown",
#                 "database_created": False,
#                 "timestamp": end_time.isoformat(),
#             }

#     def _update_github_tasks_repository(self, repository: str):
#         """Update GitHub tasks to use the specified repository"""

#         # Update GitHub issues task
#         self.tasks["github_issues"].description = self.tasks[
#             "github_issues"
#         ].description.replace(settings.TARGET_REPOSITORY, repository)

#         # Update GitHub PRs task
#         self.tasks["github_prs"].description = self.tasks[
#             "github_prs"
#         ].description.replace(settings.TARGET_REPOSITORY, repository)

#     def get_workflow_info(self):
#         """Get information about the combined workflow setup"""

#         return {
#             "total_agents": 2,
#             "agents": [self.github_agent.role, self.notion_agent.role],
#             "total_tasks": len(self.tasks),
#             "github_tasks": ["github_issues", "github_prs", "github_analysis"],
#             "notion_tasks": ["notion_search", "notion_database", "notion_insert"],
#             "process_type": "sequential",
#             "data_flow": "GitHub → Notion",
#             "target_repository": settings.TARGET_REPOSITORY,
#         }

#     def get_execution_summary(self, result):
#         """Get a summary of the execution results"""

#         if result["success"]:
#             return {
#                 "status": "✅ SUCCESS",
#                 "github_data_fetched": True,
#                 "notion_database_created": True,
#                 "data_inserted": True,
#                 "execution_time": f"{result['execution_time']:.2f}s",
#                 "repository": result["repository"],
#             }
#         else:
#             return {
#                 "status": "❌ FAILED",
#                 "error": result["error"],
#                 "execution_time": f"{result['execution_time']:.2f}s",
#                 "repository": result["repository"],
#             }


# def run_github_notion_workflow(repository: str = None):
#     """Convenience function to run the combined GitHub + Notion workflow"""

#     orchestrator = GitHubNotionOrchestrator()

#     # Log workflow info
#     info = orchestrator.get_workflow_info()
#     logger.info(f"📋 Workflow Info: {info}")

#     # Execute workflow
#     result = orchestrator.execute(repository)

#     # Log summary
#     summary = orchestrator.get_execution_summary(result)
#     logger.info(f"📊 Execution Summary: {summary}")

#     return result


# # Create orchestrator instance for easy import
# github_notion_orchestrator = GitHubNotionOrchestrator()

# workflow/full_orchestrator.py
"""
Complete GitHub + Notion + Calendar workflow orchestrator
Sequential process: GitHub Data → Notion Database → Calendar Bug Meetings
"""

from crewai import Crew, Process
from agents.github_agent import github_agent
from agents.notion_agent import notion_agent
from agents.calendar_agent import calendar_agent
from tasks.github_tasks import (
    fetch_issues_task,
    fetch_pull_requests_task,
    analyze_github_data_task,
)
from tasks.notion_tasks import (
    search_parent_pages_task,
    create_github_database_task,
    insert_github_data_task,
)
from tasks.calendar_tasks import (
    detect_bugs_task,
    schedule_bug_meetings_task,
    meeting_confirmation_task,
)
from config.settings import settings
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FullGitHubNotionCalendarOrchestrator:
    """Complete GitHub + Notion + Calendar workflow orchestrator"""

    def __init__(self):
        self.github_agent = github_agent
        self.notion_agent = notion_agent
        self.calendar_agent = calendar_agent
        self.tasks = self._setup_tasks()
        self.crew = self._create_crew()

    def _setup_tasks(self):
        """Setup tasks with proper context linking for complete data flow"""

        # GitHub tasks
        github_issues_task = fetch_issues_task
        github_prs_task = fetch_pull_requests_task
        github_analysis_task = analyze_github_data_task

        # Notion tasks
        notion_search_task = search_parent_pages_task
        notion_database_task = create_github_database_task
        notion_insert_task = insert_github_data_task

        # Calendar tasks
        calendar_detect_task = detect_bugs_task
        calendar_schedule_task = schedule_bug_meetings_task
        calendar_confirm_task = meeting_confirmation_task

        # Set up GitHub task context flow
        github_analysis_task.context = [github_issues_task, github_prs_task]

        # Set up Notion task context flow
        notion_database_task.context = [notion_search_task]
        notion_insert_task.context = [
            notion_search_task,  # For database ID
            notion_database_task,  # For database creation confirmation
            github_issues_task,  # For GitHub issues data
            github_prs_task,  # For GitHub PRs data
            github_analysis_task,  # For GitHub analysis results
        ]

        # Set up Calendar task context flow (gets GitHub data for bug detection)
        calendar_detect_task.context = [
            github_issues_task,  # For bug detection in issues
            github_prs_task,  # For bug detection in PRs
            github_analysis_task,  # For structured GitHub analysis
        ]
        calendar_schedule_task.context = [calendar_detect_task]
        calendar_confirm_task.context = [calendar_detect_task, calendar_schedule_task]

        return {
            # GitHub workflow (Tasks 1-3)
            "github_issues": github_issues_task,
            "github_prs": github_prs_task,
            "github_analysis": github_analysis_task,
            # Notion workflow (Tasks 4-6)
            "notion_search": notion_search_task,
            "notion_database": notion_database_task,
            "notion_insert": notion_insert_task,
            # Calendar workflow (Tasks 7-9)
            "calendar_detect": calendar_detect_task,
            "calendar_schedule": calendar_schedule_task,
            "calendar_confirm": calendar_confirm_task,
        }

    def _create_crew(self):
        """Create the CrewAI crew for complete workflow"""

        crew = Crew(
            agents=[self.github_agent, self.notion_agent, self.calendar_agent],
            tasks=list(self.tasks.values()),
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
            memory=False,  # Keep it simple for now
            max_execution_time=1200,  # 20 minutes total timeout
        )

        logger.info(
            "✅ Complete GitHub + Notion + Calendar crew created with sequential process"
        )
        return crew

    def execute(self, repository: str = None):
        """Execute the complete GitHub + Notion + Calendar workflow"""

        target_repo = repository or settings.TARGET_REPOSITORY

        logger.info("🚀 Starting Complete GitHub + Notion + Calendar workflow...")
        logger.info(f"📂 Target repository: {target_repo}")
        logger.info("🔄 Flow: GitHub Data → Notion Database → Bug Meetings")
        logger.info(
            f"📧 Meeting invitations sent to: {settings.DEFAULT_ATTENDEE_EMAIL}"
        )
        logger.info(f"⏰ Meetings scheduled 24 hours from execution time")

        start_time = datetime.now()

        try:
            # Update GitHub tasks with target repository
            self._update_github_tasks_repository(target_repo)

            # Execute the crew workflow
            result = self.crew.kickoff()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.info(
                f"✅ Complete workflow completed in {execution_time:.2f} seconds"
            )

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "repository": target_repo,
                "github_agent": "completed",
                "notion_agent": "completed",
                "calendar_agent": "completed",
                "database_created": True,
                "meetings_scheduled": True,
                "meeting_recipient": settings.DEFAULT_ATTENDEE_EMAIL,
                "timestamp": end_time.isoformat(),
            }

        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.error(
                f"❌ Complete workflow failed after {execution_time:.2f} seconds: {e}"
            )

            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "repository": target_repo,
                "github_agent": "unknown",
                "notion_agent": "unknown",
                "calendar_agent": "unknown",
                "database_created": False,
                "meetings_scheduled": False,
                "meeting_recipient": settings.DEFAULT_ATTENDEE_EMAIL,
                "timestamp": end_time.isoformat(),
            }

    def _update_github_tasks_repository(self, repository: str):
        """Update GitHub tasks to use the specified repository"""

        # Update GitHub issues task
        self.tasks["github_issues"].description = self.tasks[
            "github_issues"
        ].description.replace(settings.TARGET_REPOSITORY, repository)

        # Update GitHub PRs task
        self.tasks["github_prs"].description = self.tasks[
            "github_prs"
        ].description.replace(settings.TARGET_REPOSITORY, repository)

    def get_workflow_info(self):
        """Get information about the complete workflow setup"""

        return {
            "total_agents": 3,
            "agents": [
                self.github_agent.role,
                self.notion_agent.role,
                self.calendar_agent.role,
            ],
            "total_tasks": len(self.tasks),
            "github_tasks": ["github_issues", "github_prs", "github_analysis"],
            "notion_tasks": ["notion_search", "notion_database", "notion_insert"],
            "calendar_tasks": [
                "calendar_detect",
                "calendar_schedule",
                "calendar_confirm",
            ],
            "process_type": "sequential",
            "data_flow": "GitHub → Notion → Calendar",
            "target_repository": settings.TARGET_REPOSITORY,
            "meeting_recipient": settings.DEFAULT_ATTENDEE_EMAIL,
            "meeting_duration": settings.MEETING_DURATION_MINUTES,
            "bug_label": settings.BUG_LABEL,
        }

    def get_execution_summary(self, result):
        """Get a summary of the execution results"""

        if result["success"]:
            return {
                "status": "✅ SUCCESS",
                "github_data_fetched": True,
                "notion_database_created": True,
                "data_inserted": True,
                "bugs_detected": True,
                "meetings_scheduled": result["meetings_scheduled"],
                "meeting_recipient": result["meeting_recipient"],
                "execution_time": f"{result['execution_time']:.2f}s",
                "repository": result["repository"],
            }
        else:
            return {
                "status": "❌ FAILED",
                "error": result["error"],
                "execution_time": f"{result['execution_time']:.2f}s",
                "repository": result["repository"],
            }


def run_complete_workflow(repository: str = None):
    """Convenience function to run the complete GitHub + Notion + Calendar workflow"""

    orchestrator = FullGitHubNotionCalendarOrchestrator()

    # Log workflow info
    info = orchestrator.get_workflow_info()
    logger.info(f"📋 Complete Workflow Info: {info}")

    # Execute workflow
    result = orchestrator.execute(repository)

    # Log summary
    summary = orchestrator.get_execution_summary(result)
    logger.info(f"📊 Execution Summary: {summary}")

    return result


# Create orchestrator instance for easy import
complete_orchestrator = FullGitHubNotionCalendarOrchestrator()
