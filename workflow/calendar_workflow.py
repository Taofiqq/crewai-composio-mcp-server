# workflow/calendar_workflow.py
"""
Calendar bug meeting workflow using CrewAI
Sequential process: Detect Bugs → Schedule Meetings → Confirm Results
Sends meeting invitations ONLY to abumahfuz21@gmail.com
"""

from crewai import Crew, Process
from agents.calendar_agent import calendar_agent
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


class CalendarBugWorkflow:
    """Calendar bug meeting scheduling workflow"""

    def __init__(self):
        self.agent = calendar_agent
        self.tasks = self._setup_tasks()
        self.crew = self._create_crew()

    def _setup_tasks(self):
        """Setup tasks with proper context linking"""

        # Create fresh task instances
        detection_task = detect_bugs_task
        scheduling_task = schedule_bug_meetings_task
        confirmation_task = meeting_confirmation_task

        # Set up context flow: each task uses output from previous
        scheduling_task.context = [detection_task]
        confirmation_task.context = [detection_task, scheduling_task]

        return {
            "detection": detection_task,
            "scheduling": scheduling_task,
            "confirmation": confirmation_task,
        }

    def _create_crew(self):
        """Create the CrewAI crew for Calendar bug workflow"""

        crew = Crew(
            agents=[self.agent],
            tasks=list(self.tasks.values()),
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
            memory=False,  # Keep it simple for now
            max_execution_time=600,  # 10 minutes total timeout
        )

        logger.info("✅ Calendar bug crew created with sequential process")
        return crew

    def execute_with_github_data(self, github_data: str):
        """Execute the Calendar bug workflow with GitHub data as input"""

        logger.info("🚀 Starting Calendar bug meeting workflow...")
        logger.info(f"📅 Meeting duration: {settings.MEETING_DURATION_MINUTES} minutes")
        logger.info(f"🔍 Looking for '{settings.BUG_LABEL}' labels")
        logger.info(
            f"📧 Sending invitations ONLY to: {settings.DEFAULT_ATTENDEE_EMAIL}"
        )

        start_time = datetime.now()

        try:
            # Inject GitHub data into the detection task's description
            enriched_description = f"""
            {self.tasks['detection'].description}
            
            GitHub Data to Analyze for Bugs:
            {github_data}
            """

            # Update the detection task with GitHub data
            self.tasks["detection"].description = enriched_description

            # Execute the crew workflow
            result = self.crew.kickoff()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.info(
                f"✅ Calendar bug workflow completed in {execution_time:.2f} seconds"
            )

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "bug_label": settings.BUG_LABEL,
                "meeting_duration": settings.MEETING_DURATION_MINUTES,
                "recipient_email": settings.DEFAULT_ATTENDEE_EMAIL,
                "timestamp": end_time.isoformat(),
            }

        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.error(
                f"❌ Calendar bug workflow failed after {execution_time:.2f} seconds: {e}"
            )

            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "bug_label": settings.BUG_LABEL,
                "meeting_duration": settings.MEETING_DURATION_MINUTES,
                "recipient_email": settings.DEFAULT_ATTENDEE_EMAIL,
                "timestamp": end_time.isoformat(),
            }

    def execute_standalone(self):
        """Execute Calendar workflow with sample GitHub bug data for testing"""

        # Sample GitHub data with bugs for standalone testing
        sample_github_data = f"""
        GitHub Analysis Results from {settings.TARGET_REPOSITORY}:
        
        ISSUES FOUND:
        1. Issue #1: "Making Composio work"
           - Labels: ['bug', 'urgent']
           - Assignees: ['Taofiqq']
           - State: open
           - Created: 2025-06-08
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
           - State: open
           - Created: 2025-06-16
           - Repository: {settings.TARGET_REPOSITORY}
        
        BUG SUMMARY:
        - Total bug-labeled items: 3
        - Critical bugs: 1 (security vulnerability)
        - Urgent bugs: 1 (Composio integration)
        - All bugs are currently open and need attention
        """

        return self.execute_with_github_data(sample_github_data)

    def get_workflow_info(self):
        """Get information about the workflow setup"""

        return {
            "agent_role": self.agent.role,
            "total_tasks": len(self.tasks),
            "task_names": list(self.tasks.keys()),
            "process_type": "sequential",
            "meeting_duration": settings.MEETING_DURATION_MINUTES,
            "bug_label": settings.BUG_LABEL,
            "recipient_email": settings.DEFAULT_ATTENDEE_EMAIL,
            "meeting_schedule": "24 hours from execution time",
        }


def run_calendar_bug_workflow_standalone():
    """Convenience function to run the Calendar bug workflow standalone"""

    workflow = CalendarBugWorkflow()

    # Log workflow info
    info = workflow.get_workflow_info()
    logger.info(f"📋 Workflow Info: {info}")

    # Execute workflow with sample bug data
    return workflow.execute_standalone()


def run_calendar_bug_workflow_with_data(github_data: str):
    """Convenience function to run Calendar bug workflow with provided GitHub data"""

    workflow = CalendarBugWorkflow()
    return workflow.execute_with_github_data(github_data)


# Create workflow instance for easy import
calendar_bug_workflow = CalendarBugWorkflow()
