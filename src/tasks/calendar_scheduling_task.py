from crewai import Task
from config.settings import USER_EMAIL
from datetime import datetime


def create_calendar_scheduling_task(calendar_agent):
    """Create task for scheduling meetings based on analysis"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    return Task(
        description=f"""
        Schedule appropriate meetings based on the GitHub analysis and Notion documentation:
        
        CRITICAL INSTRUCTIONS:
        1. Today's date is {current_date} - schedule meetings in the FUTURE only
        2. ALWAYS include {USER_EMAIL} as an attendee
        3. Determine if a meeting is needed based on severity and complexity
        4. Calculate appropriate meeting duration (30-90 minutes)
        5. Identify required attendees from stakeholder analysis
        6. Schedule meeting within appropriate timeframe based on priority:
           - Critical: Within 1-2 days from today
           - High: Within 2-3 days from today
           - Medium: Within 3-5 days from today
        7. Create meeting agenda referencing the Notion documentation
        8. Set up calendar event with proper details and invitations
        9. Use business hours (9 AM - 5 PM) for scheduling
        """,
        agent=calendar_agent,
        expected_output=f"""
        Meeting scheduling result:
        - Decision: Meeting needed (yes/no)
        - If yes: Calendar event details including
          - Meeting title and agenda
          - Scheduled date and time (FUTURE date after {current_date})
          - Duration and attendees (including {USER_EMAIL})
          - Event ID and meeting link
        - If no: Explanation of why no meeting is needed
        """,
    )
