# tasks/calendar_tasks.py
"""
Calendar-specific tasks for bug meeting scheduling
Sends meeting invitations ONLY to abumahfuz21@gmail.com when bugs are detected
"""

from crewai import Task
from agents.calendar_agent import calendar_agent
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalendarTasks:
    """Container class for Calendar-related bug meeting tasks"""

    @staticmethod
    def detect_bugs_task() -> Task:
        """Task to analyze GitHub data and identify bug-labeled items"""

        task = Task(
            description=f"""
            Analyze the GitHub issues and pull requests data to identify items labeled with '{settings.BUG_LABEL}' or similar critical labels.
            
            Requirements:
            1. Review all GitHub issues and PRs provided in the context
            2. Identify items specifically labeled with '{settings.BUG_LABEL}', 'critical', 'urgent', or 'security'
            3. Extract key information for each bug:
               - Issue/PR title and number
               - Labels that indicate severity
               - Current state (open/closed)
               - Created date
               - Brief description
            4. Determine which bugs need immediate meetings
            5. Prioritize critical and urgent bugs
            
            Focus on:
            - Active bugs (open state)
            - Critical security issues
            - Urgent performance problems
            - High-priority frontend/backend bugs
            """,
            expected_output="""
            A structured bug analysis report containing:
            - Total number of bug-labeled items found
            - List of bugs requiring immediate meetings with details:
              * Bug title and number
              * Severity level based on labels
              * Reason why a meeting is needed
              * Recommended meeting urgency (immediate, within 24h)
            - Summary of critical bugs that need attention
            
            Format as a clear report identifying which bugs need meetings scheduled.
            """,
            agent=calendar_agent,
            context=[],  # Will be populated with GitHub data from previous tasks
        )

        logger.info("✅ Calendar bug detection task created")
        return task

    @staticmethod
    def schedule_bug_meetings_task() -> Task:
        """Task to schedule actual calendar meetings for detected bugs"""

        task = Task(
            description=f"""
            Create Google Calendar meetings for the bug-labeled items identified in the previous analysis.
            
            CRITICAL REQUIREMENTS:
            1. For each bug requiring a meeting:
               - Create a descriptive meeting title: "Bug Review: [Issue Title] (#[Number])"
               - Set meeting duration to exactly {settings.MEETING_DURATION_MINUTES} minutes
               - Schedule for exactly 24 hours from the current date and time
               - Add ONLY one attendee: "{settings.DEFAULT_ATTENDEE_EMAIL}"
               - Include comprehensive GitHub context in meeting description
            
            2. Meeting description must include:
               - GitHub issue/PR URL
               - Bug description and labels
               - Current status and severity
               - Expected discussion points
               - Repository information
            
            3. Meeting details format:
               - Title: "Bug Review: [Bug Title] (#[Number])"
               - Duration: {settings.MEETING_DURATION_MINUTES} minutes
               - Attendees: ["{settings.DEFAULT_ATTENDEE_EMAIL}"] (ONLY this email)
               - Start time: Current time + 24 hours in YYYY-MM-DDTHH:MM:SS format
            
            IMPORTANT RULES:
            - Use exact action name: GOOGLECALENDAR_CREATE_EVENT
            - Send invitations ONLY to "{settings.DEFAULT_ATTENDEE_EMAIL}"
            - Do NOT include any GitHub assignees, reviewers, or authors
            - Schedule exactly 24 hours from current time
            - Create one meeting per bug-labeled item
            """,
            expected_output="""
            A summary of scheduled bug meetings containing:
            - Number of bug meetings created
            - Details for each scheduled meeting:
              * Meeting title and Google Calendar event ID
              * Scheduled date and time (24 hours from now)
              * Attendee confirmation (only abumahfuz21@gmail.com)
              * GitHub context included in description
            - Google Calendar event links for verification
            - Confirmation of successful meeting creation
            
            Include verification that meetings were sent only to the specified email address.
            """,
            agent=calendar_agent,
            tools=calendar_agent.tools,
            context=[],  # Will be populated with bug analysis results
        )

        logger.info("✅ Calendar bug meeting scheduling task created")
        return task

    @staticmethod
    def meeting_confirmation_task() -> Task:
        """Task to provide confirmation of scheduled bug meetings"""

        task = Task(
            description=f"""
            Provide a final confirmation summary of all bug meetings scheduled.
            
            Requirements:
            1. Summarize all meetings created for bug-labeled items
            2. Confirm that meetings were sent only to "{settings.DEFAULT_ATTENDEE_EMAIL}"
            3. List meeting times and GitHub issues covered
            4. Provide actionable next steps for bug resolution
            5. Note any bugs that couldn't be scheduled
            
            Focus on providing clear confirmation and follow-up information.
            """,
            expected_output="""
            A final confirmation report containing:
            - Total bug meetings scheduled
            - Meeting schedule for the next 24-48 hours
            - Confirmation that all invitations went to {settings.DEFAULT_ATTENDEE_EMAIL} only
            - List of GitHub bugs covered in meetings
            - Next steps for bug resolution and follow-up
            - Any scheduling issues or recommendations
            
            Format as a professional summary for bug tracking and resolution.
            """,
            agent=calendar_agent,
            context=[],  # Will be populated with previous task outputs
        )

        logger.info("✅ Calendar meeting confirmation task created")
        return task


# Create task instances for easy import
calendar_tasks = CalendarTasks()

# Individual task instances
detect_bugs_task = calendar_tasks.detect_bugs_task()
schedule_bug_meetings_task = calendar_tasks.schedule_bug_meetings_task()
meeting_confirmation_task = calendar_tasks.meeting_confirmation_task()
